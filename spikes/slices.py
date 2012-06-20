import os
import subprocess

def createSlices(height,output,path,step,layer_thickness):
	#height=5
	#output="trololo.jpg"
	#path=os.path.abspath("C:/Users/Leonardo/Documents/Helix.stl")
	#print path
	#step=0.5
	#layer_thickness=10
	dir=output[:(-len(output)+output.find('.'))]
	#print dir
	if not (os.path.exists(dir)):
		os.mkdir(dir)
	os.chdir(dir)
	#os.system("slice "+path+" -z0,"+str(height)+",0.5 -o "+output)
	os.system("slice "+path+" -z0,"+str(height)+","+str(step)+" -l "+str(layer_thickness)+" -o "+output)


#height = raw_input("Enter height: ")
#output = raw_input("Enter output: ")
#path = raw_input("Enter stl absolute path: ")
#step = raw_input("Enter step: ")
#layer_thickness = raw_input("Enter layer thickness: ")
#createSlices(height,output,path,step,layer_thickness)