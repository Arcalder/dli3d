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
    def testUseSomeWeirdClass(self, mocking_not_implemented_class):
        # Arrange
        # Act
        methodWithNotImplementedClass()
        # Assert
        mocking_not_implemented_class.assert_called_with()
        mocking_not_implemented_class.not_implemented_method.foo.has_been_called()
