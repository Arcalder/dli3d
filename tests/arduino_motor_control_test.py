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
		mock_arduino_motor_control_class.assert_called_with(PORT, 9600)
		self.assertTrue(arduino is not None)

	@patch('serial.Serial')
	def testMoveUp(self, mock_arduino_motor_control_class):
		#arrange
		PORT = 'COM6'
		arduino = ArduinoMotorControl(PORT)
		mock_arduino_motor_control_class.write('.').return_value = None
		# Act
		result = arduino.move_up()
		#assert
		self.assertTrue(arduino is not None)
		mock_arduino_motor_control_class.write.assert_called_with('.')
	
	@patch('serial.Serial')
	def testMoveDown(self, mock_arduino_motor_control_class):
		#arrange
		PORT = 'COM6'
		arduino = ArduinoMotorControl(PORT)
		mock_arduino_motor_control_class.write('-').return_value = None
		#act
		arduino.move_down()
		#assert
		self.assertTrue(arduino is not None)
		mock_arduino_motor_control_class.write.assert_called_with('-')

	@patch('serial.Serial')
	def testMoveUpSteps(self, mock_arduino_motor_control_class):
		#arrange
		PORT = 'COM6'
		arduino = ArduinoMotorControl(PORT)
		mock_arduino_motor_control_class.write('10u').return_value = None
		#act
		arduino.move_up_steps(10)
		#assert
		self.assertTrue(arduino is not None)
		mock_arduino_motor_control_class.write.assert_called_with('10u')

	@patch('serial.Serial')
	def testMoveDownSteps(self, mock_arduino_motor_control_class):
		#arrange
		PORT = 'COM6'
		arduino = ArduinoMotorControl(PORT)
		mock_arduino_motor_control_class.write('10d').return_value = None
		#act
		arduino.move_down_steps(10)
		#assert
		self.assertTrue(arduino is not None)
		mock_arduino_motor_control_class.write.assert_called_with('10d')

	@patch('serial.Serial')
	def TestCloseValve(self, mock_arduino_motor_control_class):
		#arrange
		PORT = 'COM6'
		arduino = ArduinoMotorControl(PORT)
		mock_arduino_motor_control_class.write('c').return_value = None
		#act
		arduino.close_valve()
		#assert
		self.assertTrue(arduino is not None)
		mock_arduino_motor_control_class.write.assert_called_with('c')

	@patch('serial.Serial')
	def TestOpenValve(self, mock_arduino_motor_control_class):
		#arrange
		PORT = 'COM6'
		arduino = ArduinoMotorControl(PORT)
		mock_arduino_motor_control_class.write('o').return_value = None
		#act
		arduino.open_valve()
		#assert
		self.assertTrue(arduino is not None)
		mock_arduino_motor_control_class.write.assert_called_with('o')
		
	@patch('serial.Serial')
	def testOpenCloseValve(self, mock_arduino_motor_control_class):
		#arrange
		PORT = 'COM6'
		time_open = 0.5
		arduino = ArduinoMotorControl(PORT)
		mock_arduino_motor_control_class.write('o').return_value = None
		#act
		arduino.open_close_valve(time_open)
		#assert
		self.assertTrue(arduino is not None)
		#mock_arduino_motor_control_class.write.assert_called_with('o')
