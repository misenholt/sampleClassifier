'''
Created on Mar 19, 2017

@author: Max
'''
import os

saveToBucket = False
bucketName = 'misenholt-patent-data'
data_loc = os.path.sep.join((os.getcwd(), 'acquisition', 'data', os.path.sep))
transformerJarPath = 'D:\\dev\\sc\\SCJavaHelper\\PatentTransformer.jar'
recordsPerFile = 50000
tempFilePath = 'D:\\dev\\sc\\SCJavaHelper\\tmp'#/tmp'
maxNumProcesses = 2