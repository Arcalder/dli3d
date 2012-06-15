import os
import subprocess

#os.system("dir")
#subprocess.call(["ls", "-l"])
#os.system("slice")
def createSlices(height,output,path):
height=5
output="trololo.jpg"
stl_path="Helix.stl"
#stl_path="C:\Users\Leonardo\Documents\Helix.stl"
path=os.path.abspath("C://Users//Leonardo//Documents//Helix.stl")

#print path
os.system("echo %time%")
os.system("slice "+path+" -z0,"+str(height)+",1 -o"+output)
#os.system("slice "+stl_path+" -z0,"+str(height)+",1 -o"+output)
os.system("echo %time%")
print "Done"


hei = raw_input("Enter height: ")
out = raw_input("Enter output: ")
pat = raw_input("Enter stlpath: ")

#createSlices(hei,out,path)
output="trololo.jpg"
print output
print output.strip()

