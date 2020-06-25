import sys

if len(sys.argv) != 2 :
    print("Usage: python<X> join_download.py <Unique_download_id>")
    exit()

from client import workshop

download = workshop.joinFactory(int(sys.argv[1]))
print(f"[JOINED DOWNLOAD] UID:{download['factory_id']}")
print('[STARTING DOWNLOAD]')
workshop.resume_download(download['factory_id'], download['worker_id'])
