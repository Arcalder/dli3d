import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'lib'))

import unittest
from mock import patch

from example import giveMeSomething
from example import methodWithNotImplementedClass


class TestExample(unittest.TestCase):

    def testNone(self):
        pass

    def testGiveMeSomething(self):
        # Arrange
        # Act
        result = giveMeSomething()
        # Assert
        self.assertTrue(result is not None)

    @patch('example.NotImplementedClass')
    def testMethodWithNotImplementedClass(self, mock):
        # Arrange
        value = 'some_value'
        mock.notImplementedMethod(value).return_value = False
        # Act
        result = methodWithNotImplementedClass(value)
        # Assert
        mock.notImplementedMethod.assert_called_with(value)
        self.assertFalse(result)
