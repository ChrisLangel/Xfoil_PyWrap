import os,fnmatch   
import pylab
import numpy as np 
from pylab import loadtxt 
from math import log10,floor 
# Script that goes through all the output files, extracts information and writes it to a single python file

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


# input array and value, output index of array that is closest in value
def find_near_ind( array,value ):
	return (np.abs(array-value)).argmin()


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


# Will only load files that are in directory this is run in !!
def const_class( basename,coordfile,outfile='temp',writefile=False ): 
    xc,yc       = loadDump( coordfile ) 
    nfile       = ''.join([basename,'.nc'])  
    x,n         = loadDump( nfile )
    xu,nu,xl,nl = splitfoil( x,n,2 )
    yu,yl       = [],[]  
    mach        = 0.2
    for i in range(len(xu)):
        yu.append(yc[  find_near_ind(np.array(xc),float(xu[i])) ] )
    for i in range(len(xl)):
        yl.append(yc[  find_near_ind(np.array(xc),float(xl[i])) ] )
	
	# now go through and look for the other files for the same condition
	# have two seperate folders so the first can provide a list of unique
	# names

	# ------ Re_theta --------- # 
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
    cpfile  = ''.join([basename,'.cp'])
    cpu,cpl = cp_sort( cpfile,xu,xl ) 

	# ------ U_e --------- #
    uefile  = ''.join([basename,'.ue']) 
    ueu,uel = cp_sort( uefile,xu,xl )  

        # ------ DT ---------- # 
    topbl = ''.join([basename,'.dt']) 
    xtb,tbl = loadDump( topbl ) 
    a,dstu,b,thtu = splitbl( xtb,tbl ) 
    thtu,dstu = thtu[:len(xu)],dstu[:len(xu)] 
	
	# ------ DB ---------- # 
    topbl = ''.join([basename,'.db']) 
    xtb,bbl = loadDump( topbl ) 
    a,dstl,b,thtl = splitbl( xtb,bbl ) 
    thtl,dstl = thtl[:len(xl)],dstl[:len(xl)]
    if writefile == False:
        tempname = list( basename )  
        for i in range(len(tempname)):
            if tempname[i] == '.' : tempname[i] = '_'
            if tempname[i] == '-' : tempname[i] = 'n' 		
        tempname  = ''.join(tempname) 
        classname = ''.join(['R',tempname,'X']) 
        Rnum = ''.join( list(basename)[:9] )  
        Rey  = float(Rnum)
        return xclass(mach,Rey,xu,yu,xl,yl,nu,nl,ueu,uel,rtu,rtl,cfu,cfl,cpu,cpl,thtu,thtl,dstu,dstl)
    else:
    	# Create a bunch of strings to write to file
        xu   = ''.join(['xu = '  ,str(xu)  ,'\n'])
        yu   = ''.join(['yu = '  ,str(yu)  ,'\n'])
        xl   = ''.join(['xl = '  ,str(xl)  ,'\n'])
        yl   = ''.join(['yl = '  ,str(yl)  ,'\n'])
        nu   = ''.join(['nu = '  ,str(nu)  ,'\n'])
        nl   = ''.join(['nl = '  ,str(nl)  ,'\n'])
        ueu  = ''.join(['ueu = ' ,str(ueu) ,'\n'])
        uel  = ''.join(['uel = ' ,str(uel) ,'\n'])
        rtu  = ''.join(['rtu = ' ,str(rtu) ,'\n'])
        rtl  = ''.join(['rtl = ' ,str(rtl) ,'\n'])	
        cfu  = ''.join(['cfu = ' ,str(cfu) ,'\n'])
        cfl  = ''.join(['cfl = ' ,str(cfl) ,'\n'])
        cpu  = ''.join(['cpu = ' ,str(cpu) ,'\n'])
        cpl  = ''.join(['cpl = ' ,str(cpl) ,'\n'])
        thtu = ''.join(['thtu = ',str(thtu),'\n'])
        thtl = ''.join(['thtl = ',str(thtl),'\n'])
        dstu = ''.join(['dstu = ',str(dstu),'\n'])
        dstl = ''.join(['dstl = ',str(dstl),'\n'])
        mach = ''.join(['mach = ',str(machnum),'\n']) 
    	
        # Extract reynolds number from name (will only work for O(e^6))
        Rnum = ''.join( list(basename)[:9] )  
        Rey  = ''.join(['Rey = ',Rnum,'\n' ]) 
        
        # Clean up the periods and what not in the name 
        tempname = list( basename )  
        for i in range(len(tempname)):
            if tempname[i] == '.' : tempname[i] = '_'
            if tempname[i] == '-' : tempname[i] = 'n' 		
        tempname  = ''.join(tempname) 
        classname = ''.join(['R',tempname,'X']) 
        classtr   = ''.join([classname,'= xclass(mach,Rey,xu,yu,xl,yl,nu,nl,ueu,uel,rtu,rtl,cfu,cfl,cpu,cpl,thtu,thtl,dstu,dstl)', '\n \n']) 
        varlist = [mach,Rey,xu,yu,xl,yl,nu,nl,ueu,uel,rtu,rtl,cfu,cfl,cpu,cpl,thtu,thtl,dstu,dstl]
        fd = os.open( outfile,os.O_RDWR|os.O_APPEND ) 
        for vr in varlist:
    		os.write(fd,vr) 
        os.write(fd,classtr) 
    

if __name__ == '__main__':
    # Overwrite old data if necessary 
    if os.path.exists('NXdata.py'):
    	os.remove('NXdata.py')
    
    fd = os.open('NXdata.py', os.O_RDWR|os.O_CREAT )
    os.write( fd,'#!/usr/bin/python \n' ) 
    os.write( fd,'import xclass \nfrom xclass import * \n \n' ) 
    path_to_dir = os.getcwd()
    coordfile   = 'n63.dat' 
    xc,yc       = loadDump( coordfile ) 
    
    # could get this from file but for now set here 
    machnum     = 0.2
    print path_to_dir
    
    # This will go through and create text file that corresponds to classes 
    # we use '*.nc' as a somewhat arbitrary indicator of unique cases 
    for textFile in findFiles(path_to_dir, '*.nc' ):	
        basename = os.path.splitext(os.path.basename(textFile))[0] 
        print basename
        const_class( basename,coordfile,'NXdata.py', True )
     
             
     

	
















