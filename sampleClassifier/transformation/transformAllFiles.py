'''
Created on Mar 24, 2017

@author: Max
'''
from acquisition.getAllFiles import getDownloadedFilenames
from acquisition import properties
import subprocess
import re
import os
import json
from tempfile import TemporaryFile
import multiprocessing
import boto3
import time
from random import randint

def transformAllFiles():
    fileNameList = getDownloadedFilenames()[::-1]
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(properties.bucketName)
    fileCount = 0
    for fileName in fileNameList:
        filePath = os.path.sep.join((properties.tempFilePath, fileName))
        bucket.download_file(fileName, filePath)
        if transformFile(filePath):
            cleanupFile(bucket, fileName)
            fileCount += 1
        else:
            print('Failed to transform file {fn}'.format(fn=fileName))
        
        if fileCount > 0: break
        
        
def transformFile(filePath):
    ret = subprocess.run(['java','-Xmx4g', '-jar', properties.transformerJarPath, '--input={fn}'.format(fn=filePath)])
    return ret.returncode == 0
    

def cleanupFile(bucket, fileName):
    inFilePath = os.path.sep.join(('output', re.sub('.zip$', '.bulk', fileName)))
    outFileName = re.sub('.zip$', '.json', fileName)
    data = []
    with open(inFilePath, 'r') as inFile:
        for line in inFile:
            data.append(json.loads(line))
         
    with open(outFileName, 'w') as outFile: 
        json.dump(data, outFile)

    with open(outFileName, 'rb') as outFile:
        bucket.upload_fileobj(outFile, '/'.join(('extracted', outFileName)))

    os.remove(outFileName)
    
           
    
class TransformFileProcess(multiprocessing.Process):
    
    def __init__(self, fileName):
        self.fileName = fileName
        
    def run(self):
        filePath = os.path.sep.join((properties.tempFilePath, self.fileName))
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(properties.bucketName)
        bucket.download_file(self.fileName, filePath)
        #===== Test stuff
        testOutFileName = os.path.sep.join(('output', self.fileName))
        with open(testOutFileName, 'w') as testOutFile:
            time.sleep(randint(1, 30))
            testOutFile.write('test {}'.format(self.fileName))
        #====/ Test stuff
#         if transformFile(filePath):
#             cleanupFile(bucket, self.fileName)
#         else:
#             print('Failed to transform file {fn}'.format(fn=self.fileName))

# def transformAllFiles():
#     fileNameList = getDownloadedFilenames()[::-1]
# 
#     for fileName in fileNameList:
#         tfp = TransformFileProcess(fileName)
#         tfp.run()

class multiprocessManager():
    
    def __init__(self, fileNameList):
        self.fileNameList = fileNameList
        self.processes = []
        
    def run(self):
        self.fillProcesses()
        while len(self.fileNameList) > 0:
            self.checkProcesses()
            time.sleep(5)

    def fillProcesses(self):
        
        while len(self.processes) < properties.maxNumProcesses and len(self.fileNameList) > 0:
            tfp = TransformFileProcess(self.fileNameList.pop())
            tfp.run()
            self.processes.append(tfp)
            
    def checkProcesses(self):
        for i, process in self.processes.items():
            if not process.is_alive() and len(self.fileNameList) > 0:
                tfp = TransformFileProcess(self.fileNameList.pop())
                tfp.run()
                self.processes[i] = tfp
        

if __name__ == '__main__':
    transformAllFiles()
#     fn = '2003_pg030107.zip'
#     s3 = boto3.resource('s3')
#     bucket = s3.Bucket(properties.bucketName)
#     cleanupFile(bucket, fn)