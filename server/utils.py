import config
import requests
import math



def get_work_size(f_size):
    '''
     return size of work using formula
     file size range = base_f_size * ( 2**(i*3) , 2**((i+1)*3) ]
     and corresponding work size = base_work_size * 2**i
    '''
    w_conf = config.WORK
    max_index = w_conf.get('max_f_size_index')
    bfs = pow(2, w_conf.get('base_f_size'))
    bws = pow(2, w_conf.get('base_w_size'))

    if f_size <= bfs:
        return -1
    
    for i in range(max_index):
        if f_size > bfs*pow(2,i*3) and f_size <= bfs*pow(2,(i+1)*3):
            break

    return bws*pow(2,i)


def get_file_info(url):
    '''
    Return size of the file 
    or -1 if size not available
    '''
    res = requests.head(url)
    fsize = int(res.headers.get('content-length' , -1))
    fname = res.url.split("/")[-1]
    return {
        'file_size' : fsize,
        'file_name' : fname
    }

def get_range(f_size, w_size, w_id):
    #total_work = math.ceil(f_size/w_size)
    a = w_size*w_id
    b = min( w_size*(w_id+1)-1, f_size - 1 )
    return [a,b]

#Testing
# print(get_file_info('https://file-examples.com/wp-content/uploads/2017/11/file_example_MP3_5MG.mp3'))