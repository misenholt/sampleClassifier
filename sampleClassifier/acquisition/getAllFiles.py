# -*- coding: utf-8 -*-
import re
from urllib.request import urlretrieve
from acquisition import properties
import boto3
import os


def getAllFiles():
    urls = getUrls()
    for url in urls:
        getFile(url)

def getFile(url):
    fn = getFNFromURL(url)
    # get file from web
#     with urlretrieve(url) as (local_filename, h):
    local_filename, h = urlretrieve(url)
    if properties.saveToBucket == False:
        saveFileFS(local_filename, fn)
    else:
        saveFileS3(local_filename, properties.bucketName, fn)


def getUrls():
#     urls = []
#     with open('html', 'r') as html:
#         with open('downloadURLs', 'w') as urlFile:
#          
#             for line in html:
#                 m = re.search('<a href="(.*)">', line)
#                 if m:
#                     urlFile.write(m.group(1) + '\n')

    urls = []
#     urlFile = open('downloadURLs', 'r')
    with open(os.path.sep.join((properties.data_loc, 'downloadURLs')), 'r') as urlFile:
        for url in urlFile:
            urls.append(url.strip())
        
    return urls

def getFNFromURL(url):
    m = re.search('grant_full_text\/(.*)$', url)
    return m.group(1).replace(r'/', '_')
    

def saveFileFS(local_filename, filename):
    with open(local_filename, 'rb') as local_file, open(filename, 'wb') as dest_file:
        dest_file.write(local_file.read())

def saveFileS3(local_filename, filename, bucket):
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(local_filename, bucket, filename)