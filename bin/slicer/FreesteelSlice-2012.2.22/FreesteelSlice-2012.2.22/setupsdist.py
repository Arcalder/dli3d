#!/usr/bin/env python

# to set up a source distribution on linux, run
# python setupsdist.py sdist
# The result is in dist

from distutils.core import setup

setup(name='FreesteelSlice',
      version='2012.2.22',
      description='Freesteel STL slicer',
      author='Julian Todd/Martin Dunschen',
      author_email='team@pfreesteel.co.uk',
      url='http://www.freesteel.co.uk/',
      py_modules=['slice', 'savecontours', 'STLTools'],
      data_files=[('lib', ['lib/freesteelpy.py', 'lib/_freesteelpy.so', 'lib/libfreesteel.so', 'lib/libgroundsteel.so'])]
)
