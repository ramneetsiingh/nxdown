import os
import random

# Workshop Configurations
server = '127.0.0.1:8001'

api = {
    'initFactory' : '/initFactory',
    'joinFactory' : '/joinFactory',
    'getWork' : '/getWork',
    'submitWork' : '/submitWork'

}

def getURL(op):
    return 'http://' + server + api[op]

directory = {
    'APPDATA' : '/home/' + os.environ['USER'] + '/.nxdown',
    'DOWNLOAD' : '/home/' + os.environ['USER'] + '/Downloads'
}


# Merger Configurations
ports = {
    'CLIENT_PORT' : 12345,
    'SERVER_PORT' : random.randrange(10000,15000)
}

SOCKCHUNK_SIZE = 1024*10
HEADER_SIZE = 64
DISCONNECT_MSG = "!DISCONN" # 8bytes
