#-------------------------------------------------------------------------------
# Name:        TestArduino
# Author:      Eduardo & Alonso
#
# Created:     15-05-2012
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import serial
import threading
ARDUINO = 'COM6'
ser = serial.Serial(ARDUINO, 9600)

def listener():
    s = -1
    while s != 0:
        try:
            s = ser.readline()
            print s
        except Exception:
            print str(Exception)

def main():
    t = threading.Thread(target=listener)
    t.start()
    keyinput = -1
    while keyinput != 0:
        keyinput = raw_input()
        try:
           ser.write(keyinput+"\n")
        except Exception:
           print str(Exception)


if __name__ == '__main__':
    main()
