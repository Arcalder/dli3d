import os
import subprocess

def createSlices(height,output,path,step,layer_thickness):
	#height=5
	#output="trololo.jpg"
	#path=os.path.abspath("C:/Users/Leonardo/Documents/Helix.stl")
	#print path
	#step=0.5
	#layer_thickness=10
	#print height
	#print output
	#print path
	#print step
	#print layer_thickness
	dir=output[:(-len(output)+output.find('.'))]
	new_output= output[len(output)-(output[::-1]).find('\\'):]
	#print new_output
	#print dir
	if not (os.path.exists(dir)):
		os.mkdir(dir)
	#print 'Antes del chdir'+os.getcwd()
	os.chdir(dir)
	#print 'Despues del chdir'+os.getcwd()
	#os.system("slice "+path+" -z0,"+str(height)+",0.5 -o "+output)
	#print "slice "+path+" -z0,"+str(height)+","+str(step)+" -l "+str(layer_thickness)+" -o "+new_output
	os.system("slice "+path+" -z0,"+str(height)+","+str(step)+" -l "+str(layer_thickness)+" -o "+new_output)


#height = raw_input("Enter height: ")
#output = raw_input("Enter output: ")
#path = raw_input("Enter stl absolute path: ")
#step = raw_input("Enter step: ")
#layer_thickness = raw_input("Enter layer thickness: ")
#createSlices(height,output,path,step,layer_thickness)