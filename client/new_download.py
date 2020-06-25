import sys

if len(sys.argv) != 2 :
    print("Usage: python<X> new_download.py <url>")
    exit()

from workspace import workshop

download = workshop.initFactory(argv[1])
print(f"Your Unique Download ID is {download['factory_id']}")
print('[STARTING DOWNLOAD]')
workshop.resume_download(download['worker_id'])