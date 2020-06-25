import sys

if len(sys.argv) != 2 :
    print("Usage: python<X> new_download.py <url>")
    exit()

from client import workshop

download = workshop.initFactory(sys.argv[1])
print(f"Your Unique Download ID is {download['factory_id']}")
print('[STARTING DOWNLOAD]')
workshop.resume_download(download['factory_id'], download['worker_id'])
