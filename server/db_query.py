import db_init
from datetime import datetime
import random
import math

conn = db_init.nxdb.getConnection()

def init_factory(url, file_size, work_size):

    cur = conn.cursor()

    # Insert row to factory table
    cur.execute(f"insert into factory(url, file_size, work_size) values ('{url}', {file_size}, {work_size});")
    cur.execute('SELECT LASTVAL()')
    factory_id = cur.fetchone()[0]

    # Insert works to work table
    total_work = math.ceil(file_size/work_size)
    for i in range(total_work):
        cur.execute(f"insert into work(work_id, factory_id) values ('{i}', {factory_id});")

    conn.commit()
    print('[DB NEW FACTORY] New factory inserted.')

    return {
        'factory_id' : factory_id
    }


def join_factory(factory_id):
    # Insert row to worker table
    cur = conn.cursor()
    cur.execute(f"insert into worker(factory_id) values ({factory_id});")
    cur.execute('SELECT LASTVAL()')
    worker_id = cur.fetchone()[0]
    conn.commit()
    print('[DB JOIN FACTORY] worker inserted.')

    return {
        'worker_id' : worker_id
    }


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


def get_file_size(factory_id):
    cur = conn.cursor()
    cur.execute(f"select file_size from factory where factory_id = {factory_id}")
    f_size = cur.fetchone()
    if f_size is None:
        return w_size
    return f_size[0]


def get_work_size(factory_id):
    cur = conn.cursor()
    cur.execute(f"select work_size from factory where factory_id = {factory_id}")
    w_size = cur.fetchone()
    if w_size is None:
        return w_size
    return w_size[0]

def get_url(factory_id):
    # Get url of factory
    cur = conn.cursor()
    cur.execute(f"select url from factory where factory_id = {factory_id}")
    url = cur.fetchone()[0]
    return url



#Testing
# print(init_factory('www.google.com',10,3))
# print(join_factory(1))
# print(assign_work(1,2))
# print(submit_work(1,2))
# print(get_work_size(2))