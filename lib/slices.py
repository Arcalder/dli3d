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
import os
import subprocess
#sys.path.append(os.path.join(os.getcwd(), '..', 'lib'))

def createSlices(height,output,path,step,layer_thickness):
    #height=5
    #output="trololo.jpg"
    #path=os.path.abspath("C:/Users/Leonardo/Documents/Helix.stl")
    #print path
    #step=0.5
    #layer_thickness=10
    dir=output[:(-len(output)+output.find('.'))]
    #print dir
    #if not (os.path.exists(dir)):
    #   os.mkdir(dir)
    os.chdir(os.path.join('..', 'bin', 'slicer'))
    print os.getcwd()
    #os.system("slice "+path+" -z0,"+str(height)+",0.5 -o "+output)
    cmd ="slice "+path+" -z0,"+str(height)+","+str(step)+" -l "+str(layer_thickness)+" --width=800 --height=600 --background=black --core=white -o "+output
    print cmd
    os.system(cmd)
    
    
    #height = raw_input("Enter height: ")
    #output = raw_input("Enter output: ")
    #path = raw_input("Enter stl absolute path: ")
    #step = raw_input("Enter step: ")
    #layer_thickness = raw_input("Enter layer thickness: ")
    #createSlices(height,output,path,step,layer_thickness)
