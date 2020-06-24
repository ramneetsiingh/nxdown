import db_query as db
import utils

def create_factory(url):
    file_info = utils.get_file_info(url)
    f_size = file_info.get('file_size')
    f_name = file_info.get('file_name')
    work_size = utils.get_work_size(f_size)

    res = db.init_factory(url, f_name, f_size, work_size)
    print('[INTERFACE CREATE FACTORY] done.')
    return res

def join_factory(factory_id):
    print('[INTERFACE JOIN FACTORY] done.')
    return db.join_factory(factory_id)
    

def get_work(factory_id, worker_id):
    w_id = db.assign_work(factory_id, worker_id).get('work_id')
    if w_id is None:
        return {'isWork' : 0}

    f_info = db.get_factory_info(factory_id)
    f_size = f_info['file_size']
    w_size = f_info['work_size']
    [a,b] = utils.get_range(f_size, w_size, w_id)

    print('[INTERFACE GET WORK] done.')
    return{
        'isWork' : 1,
        'work_id' : w_id,
        'range_start' : a,
        'range_end' : b
    }

def submit_work(factory_id, work_id):
    db.submit_work(factory_id, work_id)
    print('[INTERFACE SUBMIT WORK] done.')