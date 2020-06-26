import sys
from client import workshop

def start(fid):
    download = workshop.joinFactory(fid)
    print(f"[JOINED DOWNLOAD] UID:{download['factory_id']}")
    print('[STARTING DOWNLOAD]')
    workshop.resume_download(download['factory_id'], download['worker_id'])
    return download['factory_id']
