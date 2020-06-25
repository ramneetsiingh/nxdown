import config
import socket

def decode_discover_message(msg):
    msg = msg.decode()
    factory_id = int(msg[0:8])
    IP = msg[8:8+15].strip('0')
    PORT = int(msg[8+15:8+15+5])
    addr = (IP,PORT)
    return {
        'factory_id' : factory_id,
        'server_addr' : addr
    }


UDPServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServer.bind(('',config.ports['CLIENT_PORT'] ))

msg = UDPServer.recvfrom(config.DISCOVER_SIZE)
print(msg)
print(decode_discover_message(msg[0]))