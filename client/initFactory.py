import requests
import config
import os

appdata_dir = config.directory.get('APPDATA')
mkdir(appdata_dir)

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def initFactory(url):
    initFactory = config.getURL('initFactory')
    r = requests.post(initFactory, json = {'url' : url}) 
    res = r.json()
    return res 

def joinFactory(f_id):
    r = requests.post(joinFactory, json = {'factory_id' : f_id}) 
    res = r.json()