# -*- coding: utf-8 -*-
import re
import urllib.request  as request
from acquisition import properties
import boto3
import os
from urllib.error import ContentTooShortError


def getAllFiles():
    urls = getUrls()
    alreadyDownloaded = getDownloadedFilenames()
#     print(properties.saveToBucket)
    for url in urls:
        if getFNFromURL(url) not in alreadyDownloaded:
            getFile(url)

def getFile(url):
    fn = getFNFromURL(url)
    # get file from web
#     with urlretrieve(url) as (local_filename, h):
    try:
        local_filename, h = request.urlretrieve(url)
    except ContentTooShortError:
        print("Failed to download from url {url}".format(url=url))
    if properties.saveToBucket:
        print('saving {fn} to bucket {bn}'.format(fn=fn, bn=properties.bucketName))
        saveFileS3(local_filename, properties.bucketName, fn)
    else:
        print('saving {fn} to file system'.format(fn=fn))
        saveFileFS(local_filename, fn)
    request.urlcleanup()


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
#     print(properties.data_loc)
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

def saveFileS3(local_filename, bucket, filename):
#     s3 = boto3.resource('s3')
#     
#     s3.meta.client.upload_file(local_filename, bucket, filename)
# ==========
#     bucket = s3.Bucket(properties.bucketName)
#     
#     with open(local_filename, 'rb') as data:
#         bucket.upload_fileobj(data, filename)
# ==============
    client = boto3.client('s3', 'us-east-1')
    transfer = boto3.s3.transfer.S3Transfer(client)
    transfer.upload_file(local_filename, bucket, filename)
    
def getDownloadedFilenames():
    filenames = []
    for obj in boto3.resource('s3').Bucket(properties.bucketName).objects.all():
        filenames.append(obj.key)
    return filenames
    
if __name__ == "__main__":
#     tempfile.tempdir = '~/tmp/'
    getAllFiles()