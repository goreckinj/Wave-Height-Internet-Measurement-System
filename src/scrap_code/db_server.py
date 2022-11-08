'''
SERVER CODE FOR DB. NOT TESTED SO MIGHT NEED A FIX OR TWO
'''

import socket
import psycopg2

# TODO: Set DB And Server Stuff
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "whms"
DB_USER = "postgres"
DB_PASS = "2ztt"

S_HOST = "localhost"
S_PORT = 10000

db_con = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
db_cur = db_con.cursor()


'''
Reads num bytes from client socket and decodes to str
'''
def read_bytez(client, num):
    data = client.recv(num).decode()
    return data


'''
Parses my silly custom format for sent bytez: uid\r\ndlt\r\n\r\n
'''
def parse_custom(client):
    entry = []
    c_data = read_bytez(client, 2)
    done = False
    while not done:
        if c_data[-2:] == '\r\n':
            if len(c_data) != 2:
                entry.append(c_data[:-2])
                c_data = read_bytez(client, 2)
            else:
                done = True
        else:
            c_data += read_bytez(client, 1)
    return entry


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((S_HOST, S_PORT))
        s.listen(1)
        while True:
            client, addr = s.accept()
            with client:
                data = parse_custom(client)
                data[1] = float(data[1])
                print(data)
                # TODO: Change TABLENAME and other fields IF NECESSARY
                db_cur.execute("INSERT INTO records (uid, dlt) VALUES (%s, %s)", data)  # Could be an error but yea (uid, dlt)
                db_con.commit()
