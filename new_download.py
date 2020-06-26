import sys
from client import workshop

def start(url):
    download = workshop.initFactory(url)
    print(f"Your Unique Download ID is {download['factory_id']}")
    print('[STARTING DOWNLOAD]')
    workshop.resume_download(download['factory_id'], download['worker_id'])
    return download['factory_id']