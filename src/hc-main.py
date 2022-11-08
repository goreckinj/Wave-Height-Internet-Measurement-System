import sys
from time import sleep
from sensor.ultrasonic import distance as ultrasonic
from db.wavelogger import wavelogger
from datetime import datetime
from wifi.wifiwrapper_direct import wifiwrapper_direct
from wifi.email_service import email_notice
import sqlite3
import psycopg2
import configparser
import numpy as np

def measure(sensor):
    time = 0
    measurments = []
    while time < 20:
        measurments.append(sensor())
        sleep(0.2)
        time += 0.2
    return np.percentile(measurments, 90) - np.percentile(measurments, 10)


if __name__=="__main__":
    sensor = ultrasonic
    minutes = 0
    dist = 0
    idb = wavelogger()

    edb = wifiwrapper_direct()
    level = 0
    while True:
        level = max(level, measure(sensor))
        sleep(40)
        minutes += 1
        if(minutes == 15):
            entry = (datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), level, 0)
            estat = False
            try:
                # take care of entry
                idb.insert(entry)
                if edb.send(entry):
                    idb.set_delivered(entry[0])

                # take care of any other undelivered
                for entry in idb.select_all_undelivered():
                    edb.send(entry)
                    idb.set_delivered(entry[0])
            except sqlite3.Error as e:
                email_notice("SQLITE ERROR", e.__str__())
            except psycopg2.Error as e:
                email_notice("POSTGRES ERROR", e.__str__())
            except configparser.Error as e:
                email_notice("CONFIG ERROR", e.__str__())
            except Exception as e:
                email_notice("OTHER ERROR", e.__str__())
            minutes = 0
            level = 0



