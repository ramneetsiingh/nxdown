from . import config
import socket
from . import utils
import os

fpath = ''   # Factory Directory. Assigned in start(f,w) function

HEADER_SIZE = config.HEADER_SIZE
SOCKCHUNK_SIZE = config.SOCKCHUNK_SIZE

# Functions for communication data between server and client 
send = utils.send
recv = utils.recv

def make_header(*fields):
    '''Return HEADER ,each field of 8 bytes left padded with 0s'''
    header = ''
    for field in fields:
        header += str(field).rjust(8,'0')
    return header.ljust(HEADER_SIZE,'0').encode('utf-8')


def send_chunks(server_addr):
    '''Send Files of a factory to the Master worker'''

    # List of paths of all workers belonging to the factory
    wpath_list = [ os.path.join(fpath, dir) for dir in os.listdir(fpath) if dir.isnumeric() ]

    # Iterating for each Worker
    for wpath in wpath_list:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client.connect(server_addr)
        print(f'[CONNECTED TO SERVER] address : {server_addr}')
        print(f'[READY TO SEND DATA] worker_id : {wpath.split("/")[-1]}')

        #Sending worker ID to server
        worker_id = make_header(wpath.split('/')[-1])
        send(client, worker_id, HEADER_SIZE)

        # List of path of each file in the worker directory
        datapath_list = [ os.path.join(wpath, data) for data in os.listdir(wpath) ]
        #Iterating over each file
        for datapath in datapath_list:
            with open(datapath, 'rb') as f:
                # Reading file
                data = f.read()
                file_name = datapath.split('/')[-1]
                file_size = len(data)

                # Creating header =>  FileName(8 bytes) FileSize(8 bytes)
                data_header = make_header(file_name, file_size)

                # Sending header and file
                print(f'[SENDING DATA] File Name : {file_name} ')
                send(client, data_header, HEADER_SIZE)
                send(client, data, SOCKCHUNK_SIZE)
                print(f'[DATA SENT]')
        
        # Creating a Disconnect Message
        disconnect = make_header(config.DISCONNECT_MSG)
        send(client, disconnect, HEADER_SIZE)
        print(f'[ALL DATA SENT] worker ID : {wpath.split("/")[-1]} ')
            

# Discover Message Format => FactoryID (8 bytes) , IP (15 bytes) , PORT (5 bytes)
def decode_discover_message(msg):
    msg = msg.decode()
    factory_id = int(msg[0:8])
    IP = msg[8:8+15].lstrip('0')
    PORT = int(msg[8+15:8+15+5])
    addr = (IP,PORT)
    return {
        'factory_id' : factory_id,
        'server_addr' : addr
    }


def get_discovered(factory_id):
    '''Reeceive Discover message and return Server Addr to send files'''

    # UPD discovery listening socket
    MYIP = socket.gethostbyname(socket.gethostname())
    PORT = config.ports['CLIENT_PORT']
    ADDR = (MYIP, PORT)

    print('[WAITING TO BE DISCOVERED]')
    msg = {'factory_id' : 0}

    # Waiting while not getting discover message for corresponding FactoryID
    while msg['factory_id'] != factory_id:
        # Opening UPD socket
        UDPServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPServer.bind(('',config.ports['CLIENT_PORT'] ))

        # Receiving message
        msg = UDPServer.recvfrom(HEADER_SIZE)       # Returns tuple (Data,Addr)
        print(f'[DISCOVERED] Server UDP socket {msg[1]}')
        msg = decode_discover_message(msg[0])

    return msg['server_addr'] 


def start(factory_id):
    global fpath
    fpath = utils.factory_path(factory_id)

    # For Testing, delete it
    fpath = '/home/ramneet/.nxdown/testing'

    server_addr = get_discovered(factory_id)

    print(f'[CONNECTING TO SERVER] address : {server_addr}')
    send_chunks(server_addr)