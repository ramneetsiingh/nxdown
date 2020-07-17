from . import config
import socket
import threading
import re
from . import utils
import os
import time

fpath = ''   # Factory Directory. Assigned in start(f,w) function

# TCP socket for receiving files
MYIP = socket.gethostbyname(socket.gethostname())
PORT = config.ports['SERVER_PORT']
ADDR = (MYIP, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

HEADER_SIZE = config.HEADER_SIZE
SOCKCHUNK_SIZE = config.SOCKCHUNK_SIZE

# Functions for communication between server and client 
send = utils.send
recv = utils.recv

def receive_chunks(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected')

    # Receiving Header containing workerID
    main_header= recv(conn, HEADER_SIZE, HEADER_SIZE)
    worker_id = main_header.decode()[0:8].lstrip('0')
    print(f'[WORKER INFO] worker ID : {worker_id}')
    
    # Creating directory to Save files
    wdir = os.path.join(fpath, worker_id)
    utils.mkdir(wdir)
    
    while True:
        # Receiving header =>  FileName(8 bytes) FileSize(8 bytes) OR DISCONNECT Message
        header = recv(conn, HEADER_SIZE, HEADER_SIZE).decode()
        file_name = header[0:8].lstrip('0')
        if file_name == '':
            file_name = '0'
        file_size = int(header[8:16])

        # Checking for DISCONNECT MESSAGE
        if file_name == config.DISCONNECT_MSG:
            print(f'[ALL DATA RECEIVED] worker ID : {worker_id} ')
            break
        
        # Receiving File
        print(f'[RECEIVING DATA] File name : {file_name} ')
        data = recv(conn, file_size, SOCKCHUNK_SIZE)
        
        # Saving file to worker directory
        utils.save_data(data, wdir, file_name)
        print(f'[DATA RECEIVED]')

    conn.close()


def discover_clients(factory_id):
    # Opening UDP socket
    UDPServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Discover Message Format => FactoryID (8 bytes) , IP (15 bytes) , PORT (5 bytes)
    DISCOVER_MSG = str(factory_id).rjust(8,'0') + str(MYIP).rjust(15,'0')  + str(PORT).rjust(5,'0')
    DISCOVER_MSG = DISCOVER_MSG.ljust(HEADER_SIZE,'0')

    # Setting Broadcast Option
    UDPServer.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Broadcasting in 10 second intervals
    while True:
        UDPServer.sendto(str.encode(DISCOVER_MSG), ('<broadcast>', config.ports['CLIENT_PORT']))
        print('[DISCOVER] Broadcast on LAN')
        time.sleep(10)



def start(factory_id):
    global fpath
    fpath = utils.factory_path(factory_id)

    server.listen()
    print(f"[LISTENING] Server is listening on {ADDR}")

    discover_thread = threading.Thread(target=discover_clients, args=[factory_id])
    discover_thread.start()
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=receive_chunks, args=[conn, addr])
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        break
    thread.join()