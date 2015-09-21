#!/usr/bin/python
import numpy as np


""" A class that wil act as a container for all the variables output from XFOIL. 
Will computer derived quantities on initialization and include method for computing integrated quanties """


class xclass:
	testct = 0
	def __init__( self,xu,yu,xl,yl,nu,nl,rtu,rtl,
	              cfu,cfl,cpu,cpl,thtu,thtl,dstu,dstl ):
		self.xu   = xu
		self.yu   = yu 
		self.xl   = xl 
		self.yl   = yl
		self.nu   = nu
		self.nl   = nl 
		self.rtu  = rtu
		self.rtl  = rtl
		self.cfu  = cfu
		self.cfl  = cfl 
		self.cpu  = cpu
		self.cpl  = cpl
		self.thtu = thtu 
		self.thtl = thtl
		self.dstu = dstu
		self.dstl = dstl
		# Now compute derived quantities. Do this is in the __init__ 
		# method so this is only called once  
                self.su   = self.compsdis( self.xu,self.yu )
		self.sl   = self.compsdis( self.xl,self.yl ) 
		self.Dcpu = self.compders( self.su,self.cpu )
		self.Dcpl = self.compders( self.sl,self.cpl )
		# Just repeat the last Dcp entry so there is no error
		# when trying to plot
		self.Dcpu.append( self.Dcpu[-1] )
		self.Dcpl.append( self.Dcpl[-1] )


	def compders( self,x,y ):
		dydx = []
		for i in range(len(x)-1):
			dy = y[i+1] - y[i] 
			dx = x[i+1] - x[i]
			# avoid divide by zero mistakes 
			if dx == 0.0: dydx.append( 0.0 )
			else: dydx.append( dy/dx ) 
		return dydx


	def compsdis( self,x,y ):
		s = [ 0.0 ]
		for i in range( len(x)-1 ): 
			ds = ((y[i+1]-y[i])**2 + (x[i+1]-x[i])**2)**0.5 
			s.append( ds + s[i] ) 
		return s


        # Function that will integrate a particular quantity over a range
	# This will mostly be called when integrated over the rough region
	# Derived quanties should be computed outside this class 
	# xs,xe --- These represent the start and end of the rough region
	#           It is assumed both are positive and that xs is located 
	#           on the lower surface, and xe on the upper 
	#           function will determine the index of where this is
	# surf  --- Which surface we are on (0 -> Upper, 1 -> Lower) 
	# quant --- Want this to be the same size as xu/xl depending on
	#           what surface we are on.
	def intquant( self,xs,xe,quant,surf=0 ):
		# initialize integrated sum
		intval = 0.0 
		# Start looking for the indices we will be integrated over
		# There are a number of different cases depending on 
		# stagnation point location
		#  - First index begins on the opposite side of the foil
		#  - First index begins on same side
		# Check to see if 'quant' is the same length as 'x'
		if surf == 0: # Upper surface 
			swdr = self.switchdir(self.xu) # see if dir switches
			# determine indicies to integrate over
			stind,endind = self.findind( self.xl,xs,xe,swdr )
			# loop over these indicies 
			for i in range(stind,endind): # 
				ds     = self.su[i+1] - self.su[i] 
                                avg    = (quant[i+1] + quant[i])/2.0 
				intval += avg*ds  

		else:         # Lower surface
			swdr = self.switchdir(self.xl)
			stind,endind = self.findind( self.xl,xs,xe,swdr )
			for i in range(stind,endind): # 
				ds     = self.sl[i+1] - self.sl[i] 
                                avg    = (quant[i+1] + quant[i])/2.0 
				intval += avg*ds  
		return intval 
	

	# determine if the location of s.p. causes a change in x-dir
	def switchdir( self,x ):
		decr,swdr = False,False
		for i in range(len(x)-1):
			if (x[i+1] < x[i]): decr = True
			if (decr == True and x[i+1] > x[i]): swdr = True    
		return swdr 


	# output indices that correspond to xs,xe. Switch the order on
	# call if we are looking at lower surface.  
	def findind( self,x,xs,xe,swdr ):
		if swdr: # starting on opposite side
			if x[0] < xs: stind = 0
			else: stind = self.searchind( x,xs,1 )
			tempind = self.searchind( x[stind:],xe ) 
			endind  = tempind + stind 
		else:    # x should increase monotonically 
			stind  = 0 # Assume the roughness starts    
			endind = self.searchind( x,xe ) 
		return stind,endind    
	 

	# find first instance in array that is either greater (updown == 0) 
	# or lower (updown == 1) than given pt 
	def searchind( self,x,pt,updown=0 ):
		first  = True
		indout = 0 
		for i in range(len(x)-1):
			if updown == 0:
				if ((x[i] > pt) and first):
					indout = i
					first = False
			else:
				if ((x[i] < pt) and first):
					indout = i
					first = False
		return indout 


	
				

			










