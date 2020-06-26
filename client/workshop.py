import requests
from . import config
import os
from . import utils

appdata_dir = config.directory.get('APPDATA')
utils.mkdir(appdata_dir)

worker_path = utils.worker_path     #Function def worker_path(f_id, w_id)

#------------------------------------------------------------------------------

def init_worker_dir(head):
    factory_dir = utils.factory_path(head['factory_id'])
    worker_dir = worker_path(head['factory_id'], head['worker_id'])
    utils.mkdir(worker_dir)

    worker_id = head['worker_id']
    with open(os.path.join(worker_dir,'workerID'), 'wb') as f:
        f.write(bytes(f'{worker_id}', 'utf-8'))

    head.pop('worker_id')
    utils.write_pkl(head, os.path.join(factory_dir, "head"))
    utils.write_pkl({}, os.path.join(worker_dir, "work"))

def initFactory(url):
    initFactory = config.getURL('initFactory')
    r = requests.post(initFactory, json = {'url' : url})
    response = r.json()
    init_worker_dir(response.copy())
    return response

def joinFactory(f_id):
    joinFactory = config.getURL('joinFactory')
    r = requests.post(joinFactory, json = {'factory_id' : str(f_id)}) 
    response = r.json()
    init_worker_dir(response.copy())
    return response

#------------------------------------------------------------------------------

def update_work_file(factory_id, worker_id, key, value):
    workfile = os.path.join(worker_path(factory_id, worker_id), "work")
    work = utils.read_pkl(workfile)
    work[key] = value
    utils.write_pkl(work, workfile)

def get_work(factory_id, worker_id):    
    getWork = config.getURL('getWork')
    work = requests.post(getWork, json = {
        'factory_id' : factory_id,
        'worker_id' : worker_id
    }).json()

    if work['isWork'] == 1:
        update_work_file(factory_id, worker_id, work['work_id'], "pending")

    return work

def submit_work(factory_id, worker_id, work_id):
    update_work_file(factory_id, worker_id, work_id, "done")
    submitWork = config.getURL('submitWork')
    work = requests.post(submitWork, json = {
        'factory_id' : factory_id,
        'work_id' : work_id
    })

#------------------------------------------------------------------------------

def download(url, factory_id, worker_id, work_id, start, end):
    bytes = end-start+1
    chunk = {'Range': 'bytes={0}-{1}'.format(start, end)}
    print(f'Downloading Chunk {work_id} ({utils.size_format(bytes)})')
    r = requests.get(url, headers=chunk, stream=True) 
    
    with open(os.path.join(worker_path(factory_id, worker_id), str(work_id)), 'wb') as fp:
        fp.write(r.content)
    print('Done')

def resume_download(factory_id, worker_id):
    f_path = utils.factory_path(factory_id)
    w_path = worker_path(factory_id, worker_id)
    head = utils.read_pkl(os.path.join(f_path, "head"))
    
    with open(os.path.join(w_path,'workerID'), 'rb') as f:
        worker_id = f.read().decode('utf-8')
    factory_id = head['factory_id']
    url = head['url']

    work = get_work(factory_id, worker_id)
    while work['isWork'] == 1:
        work_id = work['work_id']
        a = work['range_start']
        b = work['range_end']
        download(url, factory_id, worker_id, work_id, a, b)
        submit_work(factory_id, worker_id, work_id)
        work = get_work(factory_id, worker_id)

#------------------------------------------------------------------------------