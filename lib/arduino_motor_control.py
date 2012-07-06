#-------------------------------------------------------------------------------
# This file is part of 'DlI3D'.
# 
# Copyright (C) 2012 by
# Ariel Calderón, Cesar Campos, Eduardo Escobar, Alvaro Faundez, Alonso Gaete,
# Felipe Gonzalez, Rodrigo Gonzalez, Roberto Riquelme, Tamara Rivera, 
# Leonardo Rojas, Maximilian Santander
# DlI3D: https://github.com/afaundez/dli3d
# 
# 'DlI3D' is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with 'DlI3D'.  If not, see <http://www.gnu.org/licenses/>.
#
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
		self.open_valve()
		time.sleep(time_open)
		self.close_valve()

