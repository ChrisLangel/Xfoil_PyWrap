import os,fnmatch   
import pylab 
from pylab import *


# Script that goes through all the .txt files, extracts information and writes it to a single pyhton file

path_to_dir = os.getcwd()

def findFiles (path, filter):
	for root, dirs, files in os.walk(path):
		for file in fnmatch.filter(files, filter):
			yield os.path.join(root, file)
# Overwrite old data if necessary 
if os.path.exists('transdict_err.py'):
	os.remove('transdict_err.py')


#Thinking this one will produce a dictionary, can have a second script that pulls data to put into polarclass
fd = os.open('transdict_err.py', os.O_RDWR|os.O_CREAT )

transdict = {}
for textFile in findFiles(path_to_dir, '*.txt'):
	den = 0 
	f = open(textFile)
	lines = f.readlines()
	bkeynamet = os.path.basename(textFile) 	
	bkeyname = list(os.path.splitext(bkeynamet)[0])
	height = bkeynamet[0:3]
	rey    = bkeynamet[-9:-6]
	if bkeynamet[0] == '1' or bkeynamet[0] == '2':
		den = bkeynamet[4:6] 
	print height,den
	for line in lines:
		if not line[0] == 'A':
			key = ''.join([str(rey), '_', str(height),'_',str(den),'_',line.split()[0][0:-2]]) 
			keylist = list(key)
			for i in range(len(keylist)):
				if keylist[i] == '.':
					keylist[i] = '_'
				if keylist[i] == '-':
					keylist[i] = 'n'
			key = ''.join(keylist)
			print key 
			transdict[key] = [line.split()[1], line.split()[2],line.split()[3]]

td = ''.join(['transdict = ',str(transdict)])
os.write(fd,td)

AoA.append(float(line.split()[0]))

trans.append(float(line.split()[1]))	
