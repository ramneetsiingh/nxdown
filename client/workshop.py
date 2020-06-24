import requests
import config
import os
import utils

appdata_dir = config.directory.get('APPDATA')
utils.mkdir(appdata_dir)

def worker_path(w_id):
    return os.path.join(appdata_dir,str(w_id))

#------------------------------------------------------------------------------

def init_worker_dir(head):
    worker_dir = worker_path(head['worker_id'])
    utils.mkdir(worker_dir)
    utils.write_pkl(head, os.path.join(worker_dir, "head"))
    utils.write_pkl({'global_status' : 'pending'}, os.path.join(worker_dir, "work"))

def initFactory(url):
    initFactory = config.getURL('initFactory')
    r = requests.post(initFactory, json = {'url' : url}) 
    response = r.json()
    init_worker_dir(response)
    return response

def joinFactory(f_id):
    joinFactory = config.getURL('joinFactory')
    r = requests.post(joinFactory, json = {'factory_id' : f_id}) 
    response = r.json()
    init_worker_dir(response)
    return response
#------------------------------------------------------------------------------

def update_work_file(worker_id, key, value):
    workfile = os.path.join(worker_path(worker_id), "work")
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
        update_work_file(worker_id, work['work_id'], "pending")
    else:
        update_work_file(worker_id, "global_status", "done")

    return work

def submit_work(factory_id, worker_id, work_id):
    update_work_file(worker_id, work_id, "done")
    submitWork = config.getURL('submitWork')
    work = requests.post(submitWork, json = {
        'factory_id' : factory_id,
        'work_id' : work_id
    })


def download(url, worker_id, work_id, start, end):
    bytes = end-start+1
    chunk = {'Range': 'bytes={0}-{1}'.format(start, end)}
    print(f'Downloading Chunk {work_id} ({utils.size_format(bytes)})')
    r = requests.get(url, headers=chunk, stream=True) 
    
    with open(os.path.join(worker_path(worker_id), str(work_id)), 'wb') as fp:
        fp.write(r.content)
    print('Done')

def resume_download(worker_id):
    head = utils.read_pkl(os.path.join(worker_path(worker_id), "head"))
    worker_id = head['worker_id']
    factory_id = head['factory_id']
    url = head['url']

    work = get_work(factory_id, worker_id)
    while work['isWork'] == 1:
        work_id = work['work_id']
        a = work['range_start']
        b = work['range_end']
        print(f'{a} {b}')
        download(url, worker_id, work_id, a, b)
        submit_work(factory_id, worker_id, work_id)
        work = get_work(factory_id, worker_id)


x = initFactory('https://file-examples.com/wp-content/uploads/2017/04/file_example_MP4_480_1_5MG.mp4')
# print(x['factory_id'])
# x = joinFactory(18)
resume_download(x['worker_id'])