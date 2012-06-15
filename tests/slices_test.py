import sys
import os
import shutil
sys.path.append(os.path.join(os.getcwd(), 'lib'))

import unittest
from slices import *

class TestSlices(unittest.TestCase):
    def testIsWorking(self):
        #Arrange
        height = 10
        step = 1
        thickness = 10
        output = "testjpg"
		#output = "C:\Users\Leonardo\Documents\dli3d"
        shutil.rmtree(output, True)
        os.mkdir(output)
        output = "../"+output
        stl = '../example stl/Helix.stl'
        #Act
        createSlices(height,output+".jpg",stl,step,thickness)
        numberOfFiles = len(os.listdir('testjpg'))
        #Assert
        self.assertTrue(numberOfFiles is not 0)

