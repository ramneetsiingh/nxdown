import requests
import config as conf
from utils import size_format

file = input('Enter URL : ')

initFactory = conf.getURL('initFactory')

r = requests.post(initFactory, json = {'url' : file}) 
res = r.json()

print ('Factory ID : ',res['factory_id'])
print ('File Name : ',res['file_name'])
f_size = size_format(res['file_size'])
print ('File Size : ', f_size)