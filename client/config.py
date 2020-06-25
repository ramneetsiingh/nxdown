import os

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
    'CLIENT_PORT' : 9876 ,
    'MASTER_PORT' : 9876
}

HEADER_SIZE = 64
DISCOVER_SIZE = 64
DISCONNECT_MSG = "!DISCONNECT"
