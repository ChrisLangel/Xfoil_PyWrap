import os,fnmatch   
import pylab
from pylab import loadtxt 

# Script that goes through all the .txt files, extracts information and writes it to a single pyhton file

path_to_dir = os.getcwd()

def findFiles (path, filter):
	for root, dirs, files in os.walk(path):
		for file in fnmatch.filter(files, filter):
			yield os.path.join(root, file)

# Overwrite old data if necessary 
if os.path.exists('s814polardata.py'):
	os.remove('s814polardata.py')

fd = os.open('s814polardata.py', os.O_RDWR|os.O_CREAT )
os.write(fd,'import polarclass \nfrom polarclass import * \n \n') 

for textFile in findFiles(path_to_dir, '*.txt'):
 	print(textFile)
	AoA,AoAt,cl,cd,trans = [],[],[],[],[]
	f = open(textFile,'r')
	for line in f:
		if not line.split()[0] == 'C':
			AoA.append(line.split()[0])
			cl.append(line.split()[1])
			cd.append(line.split()[2])
			trans.append(line.split()[5]) 
	AoA    = ''.join(['AoA = ',str(AoA),'\n'])
	cl     = ''.join(['cl = ',str(cl),'\n'])
	cd     = ''.join(['cd = ',str(cd),'\n'])
	trans  = ''.join(['trans = ',str(trans),'\n'])
	filename = os.path.basename(textFile)
	classname= list(os.path.splitext(filename)[0])
	for i in range(len(classname)):
		if classname[i] == '-' or classname[i] == '.':
			classname[i] = '_'
        classname = "".join(classname)		
	classname = ''.join(['X_',str(classname)]) 
	c_o_r = 1
	if classname[1] == 'c':
		c_o_r = 0
	# want to see if we have transition data for this case, need to figure out a way to search transition data based on name of this one 
	
	classstr = ''.join([classname, '= polar(AoA,cl,cd,',str(c_o_r),',AoA,trans,0,0)','\n','\n']) 

	os.write(fd,str(AoA))	
	os.write(fd,str(cl))
	os.write(fd,str(cd))
	os.write(fd,str(trans)) 
	os.write(fd,classstr)



