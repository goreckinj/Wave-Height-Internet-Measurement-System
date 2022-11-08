import psycopg2
import configparser
from datetime import datetime


class wifiwrapper_direct:

    '''
    Sends an entry to the external database

    entry: The entry to be sent. This method will only pull entry[0] (UID: datetime obj) and entry[1] (DLT: float)
           from the entry tuple/list.

    Return: Null

    Throws: Exception
    '''
    def send(self, entry):
        uid = entry[0]
        dlt = entry[1]

        config = configparser.ConfigParser()
        config.sections()
        config.read('whims.ini')
        edb = config['EDBSettings']

        with psycopg2.connect(host=edb['edbHost'], port=int(edb['edbPort']), dbname=edb['edbName'],
                              user=edb['edbUser'], password=edb['edbPass']) as edb:
            with edb.cursor() as edb_cur:
                edb_cur.execute("INSERT INTO records (uid, dlt) VALUES (%s, %s)", (uid, dlt))
                edb.commit()
        return True


# if __name__ == '__main__':
#     external = wifiwrapper_direct()
#     external.send((datetime.now(), 10.6543))
