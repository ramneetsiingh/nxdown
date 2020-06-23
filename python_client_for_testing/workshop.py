import os
import pickle
import requests
import config as conf
from utils import size_format


f_id = int(input('Enter Factory ID : '))
w_id = int(input('Enter your worker\'s ID : '))

chunks_path = os.path.join(os.getcwd(),conf.download['base_dir_name'])
download_path = os.path.join(chunks_path,str(w_id))

hf =  open(os.path.join(download_path,'head.pkl'), 'rb' )
head = pickle.load(hf)
hf.close()

url = head['url']
factory_id = head['factory_id']
worker_id = head['worker_id']



def download(work_id, start, end):
    bytes = end-start+1
    chunk = {'Range': 'bytes={0}-{1}'.format(start, end)}
    print(f'Downloading Chunk {work_id} ({size_format(bytes)})')
    r = requests.get(url, headers=chunk, stream=True) 
    
    with open(os.path.join(download_path, str(work_id)), 'wb') as fp:
        fp.write(r.content)
    print('Done')
    
def get_work():    
    getWork = conf.getURL('getWork')
    work = requests.post(getWork, json = {
        'factory_id' : f_id,
        'worker_id' : w_id
    })
    return work.json()

def submit_work(work_id):
    submitWork = conf.getURL('submitWork')
    work = requests.post(submitWork, json = {
        'factory_id' : f_id,
        'work_id' : work_id
    })

work = get_work()
while work['isWork'] == 1:
    work_id = work['work_id']
    a = work['range_start']
    b = work['range_end']
    download(work_id, a, b)
    submit_work(work_id)
    work = get_work()



# 19 29
