#!/usr/bin/python
# -*- coding: utf-8 -*-
from getVolumeFromPixels import countWhitePixels
import math

PIXELS_IN_A_MILIMETER = 8

class acumulator:
	def __init__(self, height):
		self.totalVolume = 0
		self.height = height
	
	def getVolume(self):
		return self.totalVolume
	def reset(self):
		self.totalVolume = 0
	def acumulate(self, imagePath):
		pixels = countWhitePixels(image)
		area = pixels*math.pow((1/PIXELS_IN_A_MILIMITER),2)
		volume = area*self.height
		self.totalVolume += volume
			
