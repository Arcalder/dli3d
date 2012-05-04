import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'lib'))

import unittest
from example import giveMeSomething


class TestExample(unittest.TestCase):

    def testNone(self):
        pass

    def testGiveMeSomething(self):
        # Arrange
        # Act
        result = giveMeSomething()
        # Assert
        self.assertTrue(result is not None)
