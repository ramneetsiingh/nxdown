import os

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
    'APPDATA' : '/home/' + os.environ['USER'] + '/.nxdown'
}