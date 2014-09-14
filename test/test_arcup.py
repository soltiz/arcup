'''
Created on 14 sept. 2014

@author: bnkeez
'''
import filecmp
from os.path import os
import unittest

import click
from click.testing import CliRunner

import arcup


class Test(unittest.TestCase):


    def setUp(self):
        #chdir to test dir so that relative resource files are resolved
        # even when test is run from an other directory
        self.previous_workdir=os.getcwd();
        os.chdir(os.path.dirname(__file__))
        
    def tearDown(self):
        os.chdir(self.previous_workdir)


    def testName(self):
        
        runner=CliRunner()
        try:
            os.remove('prerequisites-v1.out')
        except:
            pass
        result=runner.invoke(arcup.create,['"update-v1.1.zip','v1.zip','v1.1.zip' ,'prerequisites-v1.out'])
        self.assertEqual(result.exit_code, 0)
        #arcup.create(click.path("update-v1.1.zip"),"v1.zip", "v1.1.zip" ,"prerequisites.txt")
        self.assertTrue(filecmp.cmp('prerequisites-v1.out','requisites-v1.1.ref'))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()