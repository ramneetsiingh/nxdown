from . import config
from . import utils
import os

# key: workID => value: Path of file with correnponding work_id
chunks = {}

def start(factory_id):
    print('[MASTER MERGER] started')
    # Getting factory directory path
    fdir = utils.factory_path(factory_id)
    # directories in facotory directory
    ls = os.listdir(fdir)

    # Iterating over all directories 
    print('[FINDING CHUNKS]')
    for dir in ls:
        wdir = os.path.join(fdir, dir)

        # Checking if it contains data chunks. It yes, storing chunks in chunks Dictionary
        if os.path.isdir(wdir) and ('work' in os.listdir(wdir)):
            files = os.listdir(wdir)

            # Checking for only numeric file beacouse it also contain workerID and work files
            for f in files:
                if f.isnumeric():
                    chunks[int(f)] = os.path.join(wdir, f)
    
    download_file = b''

    # Ierating over chunks in sorted order and creating original download file
    print('[MERGING CHUNKS]')
    for i in sorted(chunks.keys()):
        with open(chunks[i], 'rb') as chunk:
            download_file += chunk.read()
    
    file_name = utils.read_pkl(os.path.join(fdir,'head'))['file_name']
    # Saving file to download Folder
    print('[SAVING FILE]')
    with open(os.path.join(config.directory['DOWNLOAD'], file_name), 'wb') as f:      #file_name
        f.write(download_file)

    print(f'[FILE DOWNLOADED]')