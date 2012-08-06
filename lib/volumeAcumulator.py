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
			
