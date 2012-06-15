import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'lib'))

import unittest
from mock import patch

import serial
from arduino_motor_control import *

class TestArduinoMotorControl(unittest.TestCase):

	@patch('serial.Serial')
	def testInit(self, mock_arduino_motor_control_class):
		#arrange
		PORT = 'COM6'
		#act
		arduino = ArduinoMotorControl(PORT)
		#assert
		mock_arduino_motor_control_class.assert_called_with(PORT,9600)
		self.assertTrue(arduino is not None)
		#print type(arduino.ser)
		#print type(mock_arduino_motor_control_class)
		#TODO:self.assertEqual(arduino.ser.__class__,mock_arduino_motor_control_class.__class__)