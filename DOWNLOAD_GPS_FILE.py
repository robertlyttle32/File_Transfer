#Author: Robert Lyttle
#Date: 10/22/21
#Description: download files matching file name or extension

import pysftp
import os
import time
import ftplib
import gzip
import shutil
#import pathlib
import glob
import fnmatch
import re
import logging
from pathlib import Path
from datetime import datetime


myHostname = "hostname/IP"
myUsername = "Username"
myPassword = "Password"


#myHostname = input('Enter IP address for avc: ')
#print('Enter file name or file extension you would like to download.')
#print('If file extion is used all file matching will be downloaded.')
FILE_NAME = '*.csv' #input('Enter file name or file extension: ')
#print('Enter name for directory you want to create. files will be downloaded this directory')
#tollPointDrectory = 'images' #input('Enter name: ')


def toll_point_folder():
    get_image_time = datetime.now()
    camera_sub_dir = get_image_time.strftime("%Y_%m_%d")
    return camera_sub_dir

tollPointDirectory = f'GPS_{toll_point_folder()}'

HOME = Path.home()
#MODEL = 'vehicleModel'
#path = f'{HOME}/{tollPointDrectory}_{toll_point_folder()}'
path = '/media/tti-dev-mini/ADATA HD680/'+tollPointDirectory
STORAGE_DIRECTORY = path # Storage for database, images
if os.path.exists(STORAGE_DIRECTORY):
    pass
else:
    os.mkdir(STORAGE_DIRECTORY)


remoteFilePath = '/home/pi/GPS_'+toll_point_folder()
#Define the remote path file path
#remoteFilePath = '/tmp/home/data/'
#Define the localFilePath path file path
localFilePath = STORAGE_DIRECTORY # '/home/rdl-nano2/rdl_mobile_tech/'


#logger
LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename =localFilePath+'/file_download.log',level=logging.DEBUG,format=LOG_FORMAT) #Append mode
#logging.basicConfig(filename ='/XAVIER_RELEASE/test.log',level=logging.DEBUG,format=LOG_FORMAT,filemode='w') #Overwrite mode
logger = logging.getLogger()
#logger.info('This is a test log')
#logger.debug('test debug log')
#logger.warning('test warning log')
#logger.error('test error log')
#logger.critical('test critical log')

cnopts=pysftp.CnOpts()
# - I know this next line is insecure, it's just for this test program.
cnopts.hostkeys = None


def get_gps_log():
    try:
        with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
            print("Connection succesfully established ... ")
            print('Downloading.....')
            for filename in sftp.listdir(remoteFilePath):
                if fnmatch.fnmatch(filename, FILE_NAME):
                    #print(filename)
                    saved = filename.rstrip()
                    saved = saved.split('-')
                    #print(saved[3])
                    #if count > final_count:
                    sftp.get(remoteFilePath + "/" + filename, localFilePath + "/" + filename)
    except Exception as e:
        print('lost connection')

    print()
    print('Process summary.....')
    print(datetime.now())
    print(f'Files from: {myHostname} directory {remoteFilePath}')
    logger.info(f'Files from: {myHostname} directory {remoteFilePath}')
    print(f'Files stored: {localFilePath}')
    logger.info(f'Files stored: {localFilePath}')
    print('Done.....')


def check_ping():
    os.system('clear')
    try:
        response = os.system("ping -c 4 " + myHostname)
    except Exception as e:
        print('lost connection')
    # and then check the response...
    if response == 0:
        pingstatus = "Network Active"
        print()
        print(pingstatus)
        get_gps_log()

    else:
        pingstatus = "Network Error"
        print(pingstatus)

while True:
    check_ping()
    time.sleep(1)
