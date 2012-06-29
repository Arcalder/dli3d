#!/usr/bin/python
# -*- coding: utf-8 -*-
from getVolumeFromPixels import countWhitePixels
import math

PIXELS_IN_A_MILIMETER = 8

class acumulator:
    def __init__(self, height):
        self.totalVolume = 0
        self.height = float(height)
    
    def getVolume(self):
        return self.totalVolume
    def reset(self):
        self.totalVolume = 0
    def acumulate(self, imagePath):
        pixels = countWhitePixels(imagePath)
        #print pixels
        area = pixels*math.pow((1.0/PIXELS_IN_A_MILIMETER),2.0)
        #print area
        #print self.height
        volume = area*self.height
        self.totalVolume += volume
        #print self.totalVolume
            