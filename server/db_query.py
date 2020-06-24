import db_init
from datetime import datetime
import random
import math

conn = db_init.nxdb.getConnection()

def init_factory(url,file_name ,file_size ,work_size):

    cur = conn.cursor()

    # Insert row to factory table
    cur.execute(f"insert into factory(url, file_name, file_size, work_size) values ('{url}', '{file_name}', {file_size}, {work_size});")
    cur.execute('SELECT LASTVAL()')
    factory_id = cur.fetchone()[0]

    # Insert works to work table
    total_work = math.ceil(file_size/work_size)
    for i in range(total_work):
        cur.execute(f"insert into work(work_id, factory_id) values ('{i}', {factory_id});")

    conn.commit()
    print('[DB NEW FACTORY] New factory inserted.')

    return join_factory(factory_id)


def join_factory(factory_id):
    # Insert row to worker table
    cur = conn.cursor()
    cur.execute(f"insert into worker(factory_id) values ({factory_id});")
    cur.execute('SELECT LASTVAL()')
    worker_id = cur.fetchone()[0]
    conn.commit()
    print('[DB JOIN FACTORY] worker inserted.')
    
    res = get_factory_info(factory_id)
    res['worker_id'] = worker_id
    return res


def assign_work(factory_id,worker_id):

    cur = conn.cursor()
    work_id = None

    # get unassigned work from database
    cond1_1 = f"factory_id = {factory_id} and work_status = 'unassigned'"
    cur.execute(f"select work_id from work where {cond1_1}  LIMIT 1")
    work_id = cur.fetchone()

    if work_id is None:
        return {
            'work_id' : work_id
        }

    work_id = work_id[0]
    # label it as pending and update worker
    cond2 = f"factory_id = {factory_id} and work_id = {work_id}"
    cur.execute(f"update work set work_status = 'pending', worker_id = {worker_id} where {cond2}")

    conn.commit()
    print('[DB ASSIGN WORK] work assigned.')

    return {
        'work_id' : work_id
    }


def submit_work(factory_id,work_id):
    cur = conn.cursor()
    cond = f"factory_id = {factory_id} and work_id = {work_id}"
    cur.execute(f"update work set work_status = 'done' where {cond}")
    conn.commit()
    print('[DB SUBMIT WORK] work done.')
    return 1


def get_factory_info(factory_id):
    cur = conn.cursor()
    cur.execute(f"select factory_id, url, file_name, file_size, work_size from factory where factory_id = {factory_id}")
    f_info = cur.fetchone()
    if f_info is None:
        return f_info
    return {
        'factory_id' : f_info[0],
        'url' : f_info[1],
        'file_name' : f_info[2],
        'file_size' : f_info[3],
        'work_size' : f_info[4],
    }