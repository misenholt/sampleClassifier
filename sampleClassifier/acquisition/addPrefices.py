'''
Created on Apr 3, 2017

@author: Max
'''
from acquisition.getAllFiles import getDownloadedFilenames
import boto3
from acquisition import properties
from tempfile import TemporaryFile

def addPrefix(fileName, prefix):
    s3 = boto3.resource('s3')
    obj = s3.Object(properties.bucketName, fileName)
    with TemporaryFile() as fp:
        obj.download_fileobj(fp)
        obj.delete()
        fp.seek(0)
        bucket = s3.Bucket(properties.bucketName)
        prevKey =  fileName.split('/')[-1]
        key = '/'.join((prefix, prevKey))
        print(key)
        bucket.upload_fileobj(fp, key)
    #download
    
    #delete from bucket
    
    #add prefix and upload
    
def addPrefices(prefix):    
    fileNameList = getDownloadedFilenames()
    for fileName in fileNameList:
        addPrefix(fileName, prefix)

if __name__ == '__main__':
    addPrefices('downloaded')