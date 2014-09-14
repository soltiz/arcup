'''
Created on 14 sept. 2014

@author: bnkeez
'''
import unittest
from unittestobject import UnitTestObject


class Test(unittest.TestCase):


    def testName(self):
        pass
    def test_say(self):
        testObject=UnitTestObject()
        bluc=testObject.say()
        self.assertEqual(bluc,19)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()