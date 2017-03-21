'''
Created on Mar 19, 2017

@author: Max
'''
import unittest
from acquisition.getAllFiles import getUrls, getFNFromURL, getFile
import sys


class Test(unittest.TestCase):


#     def testGetUrls(self):
#         getUrls()

    def testGetUrl(self):
        self.assertEqual(getUrls()[0], 'http://storage.googleapis.com/patents/grant_full_text/2015/ipg150106.zip')

    def testGetFN(self):
        self.assertEqual(getFNFromURL(getUrls()[0]), '2015_ipg150106.zip')

    def testGetFile(self):
        test_url = getUrls()[0]
        getFile(test_url)
        with open(getFNFromURL(test_url), 'rb') as fp:
            self.assertEqual(113726795, len(fp.read()))
            

#     def test1(self):
#         pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetUrls']
    unittest.main()