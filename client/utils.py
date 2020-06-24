import os
import pickle

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