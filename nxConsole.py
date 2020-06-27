import new_download
import join_download
from client import server_merger, client_merger, merge_master

choice = int(input('Press 1 for new download.\nPress 2 to join a download\n YOUR CHOICE : '))


def download_complete():
    print('[DOWNLOAD COMPLETE]')
    input('[MERGE PROCESS] Press Enter.')

fid = 59

if choice == 1:
    url = input('Enter URL : ')
    fid = new_download.start(url)
    download_complete()
    server_merger.start(fid)
    merge_master.start(fid)

else:
    fid = int(input('Enter UID : '))
    join_download.start(fid)
    download_complete()
    client_merger.start(fid)

# https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4

