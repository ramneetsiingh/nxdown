import config
import socket

MYIP = socket.gethostbyname(socket.gethostname())
PORT = config.ports['MASTER_PORT']
ADDR = (MYIP, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def discover_clients():
    pass


def start():
    pass
