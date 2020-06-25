import os
import pickle
from . import config

def size_format(b):
    '''Convert bytes to a representative format. Example: size_format(1024) returns "1 KB" '''
    unit = ['B','KB','MB','GB','TB']
    i = 0
    while b/1024 >= 1:
        b /= 1024
        i = i+1
    return f"{b:.3f} {unit[i]}"

def mkdir(path):
    '''make directory if does not exist'''
    if not os.path.exists(path):
        os.makedirs(path)

def write_pkl(data, file_path):
    '''Serialize data by usign pickle and save at given location'''
    with open(file_path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def read_pkl(file_path):
    '''Read pickel file and return'''
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    return data

def factory_path(f_id):
    return os.path.join(config.directory.get('APPDATA'),str(f_id))

def worker_path(f_id, w_id):
    return os.path.join(factory_path(f_id),str(w_id))


# Merger Utils

def save_chunk(data, dir_path, file_name ):
    #Example: save_file(b'Hello', '/homr/ramneet/.nxdown/<worker_id>', '<work_id>')
    mkdir(dir_path)
    with open(os.path.join(dir_path, file_name), 'rb') as f:
        f.write(data)