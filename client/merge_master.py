import config
import utils
import os

chunks = {}

def merger(factory_id):
    fdir = utils.factory_path(factory_id)
    ls = os.listdir(fdir)
    for dir in ls:
        wdir = os.path.join(fdir, dir)
        if os.path.isdir(wdir) and ('head' in os.listdir(wdir)):
            files = os.listdir(wdir)
            for f in files:
                if f.isnumeric():
                    chunks[int(f)] = os.path.join(wdir, f)
    
    download_file = b''
    for i in sorted(chunks.keys()):
        with open(chunks[i], 'rb') as chunk:
            download_file += chunk.read()
    
    with open(os.path.join(config.directory['DOWNLOAD'], 'file_name.mp4'), 'wb') as f:      #file_name
        f.write(download_file)