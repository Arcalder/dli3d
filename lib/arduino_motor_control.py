#-------------------------------------------------------------------------------
# Name:        ArduinoControl
#
# Author:      Eduardo Escobar
#
# Created:     18-05-2012
#-------------------------------------------------------------------------------
import serial

class ArduinoMotorControl():
    def __init__(self, arduino_port):
        self.ser = serial.Serial(arduino_port, 9600)

    def move_up(self):
        try:
           self.ser.write(".")
        except Exception:
           print str(Exception)
    
    def move_down(self):
        try:
           self.ser.write("-")
        except Exception:
           print str(Exception)
           
    def move_up_steps(self, steps):
        try:
           self.ser.write(steps+"u")
        except Exception:
           print str(Exception)
           
    def move_down_steps(self, steps):
        try:
           self.ser.write(steps+"d")
        except Exception:
           print str(Exception)