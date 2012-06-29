#-------------------------------------------------------------------------------
# Name:        ArduinoControl
#
# Author:      Eduardo Escobar - Roberto Riquelme - Alonso Gaete
#
# Created:     18-05-2012
#-------------------------------------------------------------------------------
import serial
import time

class ArduinoMotorControl():
	def __init__(self, arduino_port):
		try:
			self.ser = serial.Serial(arduino_port, 9600)
		except Exception:	
			print "Arduino no conectado"
	def move_up(self):
		try:
			self.ser.write(".")
		except Exception:
			print "Arduino no conectado: subiendo bandeja un step"

	def move_down(self):
		try:
			self.ser.write("-")
		except Exception:
			print "Arduino no conectado: bajando bandeja un step"

	def move_up_steps(self, steps):
		try:
			self.ser.write(str(steps)+"u")
		except Exception:
			print "Arduino no conectado: subiendo bandeja "+str(steps)+" steps"

	def move_down_steps(self, steps):
		try:
			self.ser.write(str(steps)+"d")
		except Exception:
			print "Arduino no conectado: bajando bandeja "+str(steps)+" steps"

	def close_valve(self):
		try:
			self.ser.write("c")
		except Exception:
			print "Arduino no conectado: cerrando bandeja"

	def open_valve(self):
		try:
			self.ser.write("o")
		except Exception:
			print "Arduino no conectado: abriendo bandeja"
	
	def open_close_valve(self, time_open):
		self.open_valve
		time.sleep(time_open)
		self.close_valve()

