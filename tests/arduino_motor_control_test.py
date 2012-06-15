import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'lib'))

import unittest
import serial
from arduino_motor_control import *

class TestArduinoMotorControl(unittest.TestCase):

	def testInit(self):
		#arrange
		PORT = 'COM6'
		#act
		arduino = ArduinoMotorControl(PORT)
		self.assertTrue(arduino is not None)