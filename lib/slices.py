import os
# import subprocess


def createSlices(height, output, path, step, layer_thickness):
    os.chdir(output)
    os.system("slice "+path+" -z0,"+str(height)+","+str(step)+" -l "+str(layer_thickness)+" -o "+output+".jpg")


#height = raw_input("Enter height: ")
#output = raw_input("Enter output: ")
#path = raw_input("Enter stl absolute path: ")
#step = raw_input("Enter step: ")
#layer_thickness = raw_input("Enter layer thickness: ")
#createSlices(height,output,path,step,layer_thickness)
