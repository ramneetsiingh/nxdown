import config
import socket
import threading
import re

MYIP = socket.gethostbyname(socket.gethostname())
PORT = config.ports['MASTER_PORT']
ADDR = (MYIP, PORT)
FORMAT = 'utf-8'
HEADER_SIZE = config.HEADER_SIZE

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def receive_chunks(conn, addr, work_size):
    print(f"[NEW CONNECTION] {addr} connected.")

    worker_id= int( conn.recv(HEADER_SIZE).decode()[0:8] )

    while True:
        chunk = conn.recv(HEADER_SIZE + work_size).decode()
        if chunk == config.DISCONNECT_MSG:
            print('[ALL CHUNKS RECEIVED] worker ID : {worker_id} ')
            break

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()


def discover_clients(factory_id):
    UDPServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    DISCOVER_MSG = str(factory_id).rjust(8,'0') + str(MYIP).rjust(15,'0')  + str(PORT).rjust(5,'0')
    dest_ip_prefix = re.sub('\d+$','',MYIP)
    dest_port = config.ports['CLIENT_PORT']
    for i in range(1,255):
        client_ip = dest_ip_prefix + str(i)
        client_addr = (client_ip,config.ports['CLIENT_PORT'])
        UDPServer.sendto(str.encode(DISCOVER_MSG), client_addr)
    print('[DISCOVER] Message sent to LAN')


def start(factory_id, work_size):
    server.listen()
    print(f"[LISTENING] Server is listening on {ADDR}")

    discover_thread = threading.Thread(target=discover_clients, args=[factory_id])
    discover_thread.start()
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=receive_chunks, args=[conn, addr, work_size])
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


start(8293)