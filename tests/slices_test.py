import sys
import os
import shutil

import unittest
from mock import patch

sys.path.append(os.path.join(os.getcwd(), 'lib'))
from slices import *


class TestSlices(unittest.TestCase):

    @patch('os.system')
    def testIsWorking(self, mock_os):
        #Arrange
        height = 10
        step = 1
        thickness = 10
        output = os.path.join(os.getcwd(), 'testjpg')
        shutil.rmtree(output, True)
        os.mkdir(output)
        output = os.path.join(output)
        stl = os.path.join(os.getcwd(), 'examplestl' 'Helix.stl')
        #Act
        createSlices(height, output, stl, step, thickness)
        # numberOfFiles = len(os.listdir('testjpg'))
        #Assert
        # self.assertTrue(numberOfFiles is not 0)
        mock_os.has_been_called_once()
        mock_os.assert_called_with("slice %s -z0,10,1 -l 10 -o %s.jpg" % (stl, output))
