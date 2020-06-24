import requests
import os
import pickle
import config as conf

base_path = os.getcwd()
chunks_path = os.path.join(base_path, conf.download['base_dir_name'])
if not os.path.exists(chunks_path):
    os.makedirs(chunks_path)

f_id = input('Enter Factory ID : ')
joinFactory = conf.getURL('joinFactory')
r = requests.post(joinFactory, json = {'factory_id' : f_id}) 
res = r.json()

head = {
    'factory_id' : res['factory_id'],
    'url' : res['url'],
    'worker_id' : res['worker_id']
} 

download_path = os.path.join(chunks_path, str(head['worker_id']))
os.makedirs(download_path)
os.path.join(chunks_path, str(head['worker_id']))
with open(os.path.join(download_path,'head.pkl'), 'wb') as f:
    pickle.dump(head, f, pickle.HIGHEST_PROTOCOL)

print('Your Worker\'s ID : ',head['worker_id'])