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
        ser = serial.Serial(arduino_port, 9600)

    def move_up(self):
        try:
           ser.write(".")
        except Exception:
           print str(Exception)
    
    def move_down(self):
        try:
           ser.write("-")
        except Exception:
           print str(Exception)
           
    def move_up_steps(self, steps):
        try:
           ser.write(steps+"u")
        except Exception:
           print str(Exception)
           
    def move_down_steps(self, steps):
        try:
           ser.write(steps+"d")
        except Exception:
           print str(Exception)