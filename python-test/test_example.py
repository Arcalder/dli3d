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
