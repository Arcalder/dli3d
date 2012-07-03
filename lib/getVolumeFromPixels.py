#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image

def countWhitePixels(image):
    img_I = Image.open(str(image)).getdata()
    whitePixels = 0
    for pixel in list(img_I):
       if  pixel == (255,255,255):
           whitePixels += 1
    return whitePixels