import socket

S_ADDR = 'localhost'
S_PORT = 10000

class wifiwrapper:

    def __init__(self, host, port):
        self.__HOST = host
        self.__PORT = port

    def set_host(self, host):
        self.__HOST = host

    def set_port(self, port):
        self.__PORT = port

    '''
    Sends byte string data to a host:port
    
    Return: the number 1 on successful completion
    Throws: possible exception if sendall() or s.accept() fails. To be handled at a higher level
    '''
    def send(self, bytez):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__HOST, self.__PORT))
            s.listen()
            c, addr = s.accept()
            with c:
                c.sendall(bytez)
        return 1

    '''
    Formats an entry to a json format {entry: []}
    '''
    def format_json_bytestring(self, entry):
        bytez = b'{"entry" : ["'
        bytez += entry[0].encode() + b'", '
        bytez += str(entry[1]).encode() + b']}'
        return bytez

    '''
    Formats an entry to a custom format (UID\r\nDLT\r\n\r\n)
    
    Return: a byte string in the custom format.
    '''
    def format_custom_bytestring(self, entry):
        bytez = entry[0].encode() + b'\r\n'
        bytez += str(entry[1]).encode() + b'\r\n'
        bytez += b'\r\n'
        return bytez


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (S_ADDR, S_PORT)
    client.connect(address)

    data = 'datef\r\n10.12\r\n\r\n'

    client.sendall(data.encode())
