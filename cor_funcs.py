import numpy as np
import matplotlib.pyplot as plt
from pylab import figure,plot,matplotlib
import os


# Primary correlation function F() -> int_(s.p)^(r.e) f() ds
############################################################
# Inputs:
#    k_s  -- Some "equivalent" sand grain roughness height
#    K    -- Relaminarization parameter (nu/U_e)*(dU_e/ds)
#    mutnu - Frictional velocity divided by nu (k^+ = mutnu*k_s)
#    dstar - Boundary layer diplacement thickness
#    thw  -- Thwaites pressure gradient parameter (lambda_theta)
# Output:
#       quant - Some combination of input parameters f(k^+)*g(K)
#
def comp_quant( k_s,K,mutnu,thw,dstar,mom ):
	""" Function of boundary layer quantities that will be integrated """
	quant  = []
	for i in range(len(K)):
    		kplus = mutnu[i]*k_s
		# do not add if we are outside thresholds
		if kplus < 5.0 or K[i] > 6.0e-4:
                 quant.append( float(0.0) )
		else:
			#fthws = 1.0 / (1.0 + np.exp(100.0*(thw[i]-0.0035))) + 0.5
                 #quant.append( float( kplus**4*(1.0 + 0.4*dcp[i]) ) )
                 th = float( thw[i] )
                 if th <= 0:
                     ft = 1 - (-12.9*th - 123.7*th**2 - 405.7*th**3)
                 else:
                     ft = 1 + 0.275*( 1- np.exp(-35.0*th) )
                 fthws = (ft)**4
                 #fthws = K[i]
                 #quant.append( (float( fthws*(np.exp(0.4*kplus))*dstar[i]**2.0) ) )
                 quant.append( (float( fthws*(kplus)**4*dstar[i]**(0.0) )))
	return quant






# Function that takes a string and a dictionary, then outputs a list of all the keys in the dictionary that contain that string
def get_key_list( substring,inpdict ):
	outkeys = [];
	for key in inpdict.keys():
		if substring in key: outkeys.append( key )
	return outkeys


# Take a string and a substring a return the difference
def get_str_diff( string,substring ):
	return list(string)[len(list(substring)):]


# Take in array and scalar, then return the index of the array
# that is nearest in value to scalar
def near_ind( array,value ):
	return (np.abs(array-value)).argmin()


# Function that takes in an x_class along with a target Re_theta,
# then outputs the streamwise location it occurs.
# For the time being assuming it is only the upper surface
def get_trans_ret( xclass,retcrit ):
    ret,x = xclass.rtu, xclass.xu
    rt,ct = ret[0],0
    while rt < retcrit:
        lowind  = ct
        highind = ct + 1
        ct = ct + 1
        rt = ret[ct]
    retlow,rethigh = ret[lowind],ret[highind]
    xlow,xhigh = x[lowind],x[highind]
    pct = (ret - retlow)/(rethigh - retlow)
    xout = xlow + pct*(xhigh - xlow)
    return xout


# Function that takes in x_class and outputs values of interest
# Once again assume we are on the upper surface
def extract_vars( xclass ):
    xu   = np.array( getattr( xclass, 'xu'    ) )
    su   = np.array( getattr( xclass, 'su'    ) )
    n    = np.array( getattr( xclass, 'nu'    ) )
    rt   = np.array( getattr( xclass, 'rtu'   ) )
    Dcp  = np.array( getattr( xclass, 'Dcpu'  ) )
    cf   = np.array( getattr( xclass, 'cfu'   ) )
    K    = np.array( getattr( xclass, 'Ku'    ) )
    mut  = np.array( getattr( xclass, 'mutnu' ) )
    dstr = np.array( getattr( xclass, 'dstu'  ) )
    mom  = np.array( getattr( xclass, 'thtu'  ) )
    thw  = np.array( getattr( xclass, 'Twtsu' ) )
    return xu,su,n,rt,Dcp,cf,K,mut,dstr,mom,thw


# Function that takes in x_class and outputs values of interest
# this
def extract_vars_l( xclass ):
    xl   = np.array( getattr( xclass, 'xl'    ) )
    sl   = np.array( getattr( xclass, 'sl'    ) )
    n    = np.array( getattr( xclass, 'nl'    ) )
    rt   = np.array( getattr( xclass, 'rtl'   ) )
    Dcp  = np.array( getattr( xclass, 'Dcpl'  ) )
    cf   = np.array( getattr( xclass, 'cfl'   ) )
    K    = np.array( getattr( xclass, 'Kl'    ) )
    mut  = np.array( getattr( xclass, 'mutnl' ) )
    dstr = np.array( getattr( xclass, 'dstl'  ) )
    mom  = np.array( getattr( xclass, 'thtl'  ) )
    thw  = np.array( getattr( xclass, 'Twtsl' ) )
    return xl,sl,n,rt,Dcp,cf,K,mut,dstr,mom,thw


# Function that finds the point where the slope starts to drop
def bin_arrays( xarray,yarray ):
    span = np.amax(xarray) - np.amin(xarray)
    bins = np.arange( np.amin(xarray), np.amax(xarray), span/50)
    data = np.zeros(len(bins))
    binct = np.zeros(len(bins))
    for i in range(len(bins)-1):
        for j in range(len(xarray)):
            if xarray[j] > bins[i] and xarray[j] < bins[i+1]:
                data[i] = data[i] + yarray[j]
                binct[i] = binct[i] + 1
    for i in range(len(data)):
        if binct[i] > 0:
            data[i] = data[i]/binct[i]
        else:
            data[i] = 1.0
    binmin = []
    for i in range(len(data)-1):
        if data[i] < 0.90 and data[i+1] < 0.90:
            binmin.append( bins[i+1] )
    return np.amin( binmin )



def getexp(tdict,tkey):
	AoAs,trans,sig,sigu,sigl = [],[],[],[],[]
	for k in tdict.keys():
		if str(k).startswith(tkey):
			trans.append(float(tdict[k][0]))
			sigl.append(float(tdict[k][1]))
			sigu.append(float(tdict[k][2]))
			AoAs.append(k[-4:])
	for i in range(len(AoAs)):
		atemp = list(AoAs[i])
		atemp[2] = '.'
		if atemp[0] == 'n':
			atemp[0] = '-'
			AoAs[i] = ''.join(atemp)
		else:
			AoAs[i] = ''.join(atemp[1:])
		AoAs[i] = float(AoAs[i])
	sig = [sigu,sigl]
	return AoAs,trans,sig


# input the value computed from a particular case, as well as the
# slope and y intercept of the linear correlation
# the "y" value will be the ratio of ret_rough to ret_clean
def pull_cor( val,m,b,rt,x ):
    scale = m*val + b
    # only do this if scale is less than some threshold
    if scale < 0.9:
        Rtorig = rt[-1]
        Rtrough = Rtorig*scale
        ind = near_ind(np.array(rt),Rtrough)
    else:
        ind = -1
    return x[ind]


# replace "-" with "n" and "." with "_" in string
def convert_cname(cname):
    outlist = []
    for char in list(cname):
        if char == '-':
            outlist.append('n')
        elif char == '.':
            outlist.append('_')
        else:
            outlist.append(char)
    return ''.join(outlist)


# read file with two columns, assumes they are AoA, trans
def readtrans(flabel):
	AoAs,trans = [],[]
	if os.path.exists(flabel):
		f = open(flabel)
		lines = f.readlines()
		for line in lines:
			AoAs.append(float(line.split()[0]))
			trans.append(float(line.split()[1]))
	return AoAs, trans


# function that pulls the experimental transition data for the s814 airfoil
# the format is different as error bars are not included.
def getexp_s814(tdict,tkey):
	AoAs,trans = [],[]
	for k in tdict.keys():
		if str(k).startswith(tkey):
			AoAs.append(float(tdict[k][0]))
			trans.append(float(tdict[k][1]))
	Aout, Tout = dubSort(AoAs,trans)
	return Aout, Tout

# function that takes in two arrays, returns both arrays sorted according to the
# first (e.g. [3,2,5],['eggs','butter','kale'] -> [2,3,5],['butter','eggs','kale']
def dubSort(arr1, arr2):
	atemp1 = arr1[:]
	atemp2 = []
	atemp1.sort()
	for x in atemp1:
		atemp2.append( arr2[arr1.index(x)] )
	return atemp1, atemp2
