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
import multiprocessing
import boto3
import time
from random import randint

def getTestFileNames():
    return ['test/testFile1.zip', 'test/testFile2.zip', 'test/testFile3.zip', 'test/testFile4.zip']

def transformAllFiles(test):
    if test:
        fileNameList = getTestFileNames()
    else:
        fileNameList = getDownloadedFilenames()[::-1]
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(properties.bucketName)
    fileCount = 0
    for fileName in fileNameList:
        inFilePath = os.path.sep.join((properties.tempFilePath, fileName.split('/')[-1]))
        print(inFilePath)

        bucket.download_file(fileName, inFilePath)
        if transformFile(inFilePath, test):
            cleanupFile(bucket, fileName)
            fileCount += 1
        else:
            print('Failed to transform file {fn}'.format(fn=fileName))
        
#         if fileCount > 0: break
        
        
def transformFile(filePath, test):
    if test:
        return testTransform(filePath)
    else:
        ret = subprocess.run(['java','-Xmx4g', '-jar', properties.transformerJarPath, '--input={fn}'.format(fn=filePath)])
        return ret.returncode == 0
    
def testTransform(filePath):
    try:
        outFilePath = os.path.sep.join(('output', re.sub('.zip$', '.bulk', filePath.split('/')[-1])))
        print(outFilePath)
        with open(filePath, 'r') as inFile, open(outFilePath, 'w') as outFile:
            for line in inFile:
                outFile.write(line)
                
            outFile.write('\n{"processed":1}')
        
        return True
    except Exception:
        print('Failed test transform')
        return False

def cleanupFile(bucket, fileName):
    inFilePath = os.path.sep.join(('output', re.sub('.zip$', '.bulk', fileName.split('/')[-1])))
    outFileName = re.sub('.zip$', '.json', fileName).split('/')[-1]
    data = []
    with open(inFilePath, 'r') as inFile:
        for line in inFile:
            print(line)
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
    transformAllFiles(test=True)
#     fn = '2003_pg030107.zip'
#     s3 = boto3.resource('s3')
#     bucket = s3.Bucket(properties.bucketName)
#     cleanupFile(bucket, fn)