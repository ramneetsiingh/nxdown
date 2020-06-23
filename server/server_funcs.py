import db_query as db
import utils

def create_factory(url):
    file_info = utils.get_file_info(url)
    f_size = file_info.get('file_size')
    work_size = utils.get_work_size(f_size)

    res = db.init_factory(url, f_size, work_size)
    res['file_name'] = file_info.get('file_name')
    res['file_size'] = file_info.get('file_size')
    print('[INTERFACE CREATE FACTORY] done.')
    return res

def join_factory(factory_id):
    worker_id = db.join_factory(factory_id).get('worker_id')
    url = db.get_url(factory_id)
    res = {
        'factory_id' : factory_id,
        'url' : url,
        'worker_id' : worker_id
    }
    print('[INTERFACE JOIN FACTORY] done.')
    return res
    

def get_work(factory_id, worker_id):
    f_size = db.get_file_size(factory_id)
    w_size = db.get_work_size(factory_id)
    w_id = db.assign_work(factory_id, worker_id).get('work_id')
    if w_id is None:
        return {'isWork' : 0}

    [a,b] = utils.get_range(f_size, w_size, w_id)
    return{
        'isWork' : 1,
        'work_id' : w_id,
        'range_start' : a,
        'range_end' : b
    }

def submit_work(factory_id, work_id):
    db.submit_work(factory_id, work_id)
    print('[INTERFACE SUBMIT WORK] done.')

# Testing
# print(create_factory('https://file-examples.com/wp-content/uploads/2017/11/file_example_MP3_5MG.mp3'))
# print(join_factory(4))
# submit_work(4,10)

# factory = create_factory('https://file-examples.com/wp-content/uploads/2017/11/file_example_MP3_5MG.mp3')
# print(factory)
# worker_id = factory['worker_id']
# factory_id = factory['factory_id']
# x = get_work(factory_id,worker_id)
# while x['isWork']==1:
#     print(x['range_start'] , '  ', x['range_end'])
#     x = get_work(factory_id,worker_id)