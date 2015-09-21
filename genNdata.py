import os,fnmatch   
import pylab
import numpy as np 
from pylab import loadtxt 
from math import log10,floor 

# Script that goes through all the output files, extracts information and writes it to a single pyhton file

# function that searches an input directory for files with a given filter in the title
def findFiles (path, filter):
	for root, dirs, files in os.walk(path):
		for file in fnmatch.filter(files, filter):
			yield os.path.join(root, file)

def round_sig(x, sig=2):
	if x == 0.0: return 0.0
	elif x < 0.0:
		x = -1.0*x
		return -1.0*round(x, sig-int(floor(log10(x)))-1 )
        else: return round(x, sig-int(floor(log10(x)))-1 )  


def find_near_ind( array,value ):
	idx = (np.abs(array-value)).argmin()
	return idx 


# Funtion that reads 'dump' file from XFOIL with the N-factor as output
def loadDump( file ):
	x,y = [],[] 
	lines = open(file).readlines() 
	for line in lines:
		if (len(line.split()) > 1):
			if (line.split()[0] == '#'): pass
			else:   
				x.append(float(line.split()[0]) )
				y.append(float(line.split()[1]) ) 
	return x,y 
		
# Function that splits the output into upper and lower surface
def splitfoil( x,n,comp=1 ):
	xu,xl,nu,nl = [],[],[],[]
	last,i = 0.0,0
	asplit = False
	while (asplit==False):
		if comp==1: 
			if (x[i] < last): asplit = True
			else: last = x[i]
		else: 
			if (n[i] < last): asplit = True
		        else: last = n[i]  
                i += 1 
	xu,nu = x[:i-1], n[:i-1]
	xl,nl = x[i-1:], n[i-1:]
	return xu,nu,xl,nl


def  splitbl( x,n ):
	x1,x2,n1,n2 = [],[],[],[]
	asplit = False
	xstg   = x[0]  
	i      = 1
	while (asplit==False):
		if (x[i] == xstg): asplit = True
		i += 1 
	x1,n1 = x[:i-1], n[:i-1]
	x2,n2 = x[i-1:], n[i-1:]
	return x1,n1,x2,n2


# Function that takes in cp file, as well as limited upper/lower arrays
def cp_sort( cpfile,xu,xl ):
	cpu,cpl = [],[]
        x,cpt   = loadDump( cpfile )  
	for xi in xu:
		cpu.append(cpt[find_near_ind(np.array(x),float(xi))])
	for xi in xl:
		cpl.append(cpt[find_near_ind(np.array(x),float(xi))])
        return cpu,cpl 

# ------------------------------------------------------------ #
# Overwrite old data if necessary 
if os.path.exists('Ndata.py'):
	os.remove('Ndata.py')

fd = os.open('NXdata.py', os.O_RDWR|os.O_CREAT )
os.write( fd,'#!/usr/bin/python \n' ) 
os.write( fd,'import xclass \nfrom xclass import * \n \n' ) 

path_to_dir = os.getcwd()
coordfile   = 'n63.txt' 
xc,yc       = loadDump( coordfile ) 

for textFile in findFiles(''.join([path_to_dir,'/N_data']), '*' ):	
	basename = os.path.splitext(os.path.basename(textFile))[0] 
	# Read this particular file
	x,n         = loadDump( textFile  )
	xu,nu,xl,nl = splitfoil(  x,n,2 )
        # initialize y-coord so we can compute curvalinear distance
	yu,yl       = [],[]  
	for i in range(len(xu)):
		yu.append(yc[  find_near_ind(np.array(xc),float(xu[i])) ] )
	for i in range(len(xl)):
		yl.append(yc[  find_near_ind(np.array(xc),float(xl[i])) ] )
	
	# now go through and look for the other files for the same condition
	# have two seperate folders so the first can provide a list of unique
	# names

	# ------ Re_theta --------- # 
	os.chdir( ''.join([path_to_dir,'/data_dump']) ) 
	retfile = ''.join([basename,'.rt'])
	rtu,rtl = cp_sort( retfile,xu,xl )  
	#xr,rt   = loadDump( retfile ) 
        #xru,rtu,xrl,rtl = splitfoil( xr,rt,2 )
	# only save the portion of the foil with N data. 
	rtu,rtl = rtu[:len(xu)],rtl[:len(xl)] 
 
        # ------ C_f --------- # 
	cffile = ''.join([basename,'.cf'])
	#xf,cf   = loadDump( cffile ) 
        #xcfu,cfu,xcfl,cfl = splitfoil( xf,cf )
	cfu,cfl = cp_sort( cffile,xu,xl )  
	#cfu[:len(xu)],cfl[:len(xl)] 

        # ------ C_p --------- #
	cpfile = ''.join([basename,'.cp'])
	cpu,cpl = cp_sort( cpfile,xu,xl ) 
 
        # ------ DT --------- # 
	topbl = ''.join([basename,'.dt']) 
	xtb,tbl = loadDump( topbl ) 
	a,thtu,b,dstu = splitbl( xtb,tbl ) 
        thtu,dstu = thtu[:len(xu)],dstu[:len(xu)] 
	
	# ------ DB -------- # 
	topbl = ''.join([basename,'.db']) 
	xtb,bbl = loadDump( topbl ) 
	a,thtl,b,dstl = splitbl( xtb,bbl ) 
        thtl,dstl = thtl[:len(xl)],dstl[:len(xl)]
        
	# Create a bunch of strings to write to files
	xu   = ''.join(['xu = '  ,str(xu),'\n'])
	yu   = ''.join(['yu = '  ,str(yu),'\n'])
	xl   = ''.join(['xl = '  ,str(xl),'\n'])
	yl   = ''.join(['yl = '  ,str(yl),'\n'])
	nu   = ''.join(['nu = '  ,str(nu),'\n'])
	nl   = ''.join(['nl = '  ,str(nl),'\n'])
	rtu  = ''.join(['rtu = ' ,str(rtu),'\n'])
	rtl  = ''.join(['rtl = ' ,str(rtl),'\n'])	
	cfu  = ''.join(['cfu = ' ,str(cfu),'\n'])
	cfl  = ''.join(['cfl = ' ,str(cfl),'\n'])
	cpu  = ''.join(['cpu = ' ,str(cpu),'\n'])
	cpl  = ''.join(['cpl = ' ,str(cpl),'\n'])
	thtu = ''.join(['thtu = ',str(thtu),'\n'])
	thtl = ''.join(['thtl = ',str(thtl),'\n'])
	dstu = ''.join(['dstu = ',str(dstu),'\n'])
	dstl = ''.join(['dstl = ',str(dstl),'\n'])

        # Clean up the periods and what not in the name 
        tempname = list( basename )  
	for i in range(len(tempname)):
		if tempname[i] == '.' : tempname[i] = '_'
		if tempname[i] == '-' : tempname[i] = 'n' 		
	tempname  = ''.join(tempname) 
	classname = ''.join(['R',tempname,'X']) 

	classtr   = ''.join([classname,'= xclass(xu,yu,xl,yl,nu,nl,rtu,rtl,cfu,cfl,cpu,cpl,thtu,thtl,dstu,dstl)', '\n \n']) 
	
	varlist = [xu,yu,xl,yl,nu,nl,rtu,rtl,cfu,cfl,cpu,cpl,thtu,thtl,dstu,dstl]
	for vr in varlist:
		os.write(fd,vr) 
	os.write(fd,classtr) 

	
















