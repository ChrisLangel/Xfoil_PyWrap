#!/usr/bin/python
import numpy as np


""" A class that will act as a container for all the variables output from XFOIL. 
Will computer derived quantities on initialization and include method for computing integrated quanties """


class xclass:
	#
	def __init__( self,mach,Rey,xu,yu,xl,yl,nu,nl,ueu,uel,rtu,rtl,
	                   cfu,cfl,cpu,cpl,thtu,thtl,dstu,dstl ):
		# Specify the speed of sound 
		a_0 = 340.29
		# 
		self.mach = mach
		self.Rey  = Rey 
		self.xu   = xu
		self.yu   = yu 
		self.xl   = xl 
		self.yl   = yl
		self.nu   = nu
		self.nl   = nl
		self.ueu  = ueu
		self.uel  = uel 
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
                self.su   = self.comp_sdis( self.xu,self.yu )
		self.sl   = self.comp_sdis( self.xl,self.yl ) 
		self.Dcpu = self.comp_ders( self.su,self.cpu )
		self.Dcpl = self.comp_ders( self.sl,self.cpl )
		self.Dueu = self.comp_ders( self.su,self.ueu )
		self.Duel = self.comp_ders( self.sl,self.uel )
                # Compute the relaminarization parameter 
		self.Ku    = self.comp_relam( self.mach,self.Rey,a_0,
			      	              self.ueu,self.Dueu ) 
		self.Kl    = self.comp_relam( self.mach,self.Rey,a_0,
				              self.uel,self.Duel ) 
		# Compute the Thwaites pressure gradient parameter
		self.Twtsu = self.comp_Thwaites( self.mach,self.Rey,a_0,
		      				 self.thtu,self.Dueu )
		self.Twtsl = self.comp_Thwaites( self.mach,self.Rey,a_0,
					 	 self.thtl,self.Duel )

		# Compute and store mut/nu to compute k^+ on the fly 
 		self.mutnu = self.comp_mutnu( self.cfu,Rey )
		self.mutnl = self.comp_mutnu( self.cfl,Rey ) 

	# compute forward difference derivatives of two vectors 
	def comp_ders( self,x,y ):
		dydx = [0.0] # Assume with start with a zero derivative 
		for i in range(len(x)-1):
			dy = y[i+1] - y[i] 
			dx = x[i+1] - x[i]
			# avoid divide by zero mistakes 
			if dx == 0.0: dydx.append( 0.0 )
			else: dydx.append( dy/dx ) 
		return dydx


	# compute curvilinear distance from stagnation point
	def comp_sdis( self,x,y ):
		s = [ 0.0 ]
		for i in range( len(x)-1 ): 
			ds = ((y[i+1]-y[i])**2 + (x[i+1]-x[i])**2)**0.5 
			s.append( ds + s[i] ) 
		return s


	# compute the relaminarization parameter
	def comp_relam( self,mach,Re,a_0,u_e,du_e ):
	#	a_0 = 340.29 
		nu  = (mach/Re)*a_0
		K   = [] 
		for i in range(len(du_e)):
			# Re-dimensionalize the velocities
			Ue  = a_0*float(u_e[i])
			Due = a_0*float(du_e[i])
			K.append( (nu/Ue**2)*Due )
		return K


	# compute the Thwaites pressure gradient parameter 
	def comp_Thwaites( self,mach,Re,a_0,theta,du_e ):
	#	a_0  = 340.29 
		nu   = (mach/Re)*a_0
		twts = [] 
		for i in range(len(theta)):
			twts.append( (theta[i]**2/nu)*du_e[i] )  
		return twts 


	# compute frictional velocity divided by nu to help compute k^+ 
	def comp_mutnu( self,cf,Rey ):
		mutnu = []
		for i in range(len(cf)):
			if cf[i] < 0.0: cf[i] = 0.0; 
			mutnu.append( (0.5*cf[i])**0.5*Rey ) 
		return mutnu 


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
		stot   = 0.0
		# Start looking for the indices we will be integrated over
		# There are a number of different cases depending on 
		# stagnation point location
		#  - First index begins on the opposite side of the foil
		#  - First index begins on same side
		# Check to see if 'quant' is the same length as 'x'
		if surf == 0: # Upper surface 
			swdr = self.switchdir(self.xu) # see if dir switches
			# determine indicies to integrate over
			stind,endind = self.findind( self.xu,xs,xe,swdr )
			# loop over these indicies 
			for i in range(stind,endind): # 
				ds     = self.su[i+1] - self.su[i] 
                                avg    = (quant[i+1] + quant[i])/2.0 
				intval += avg*ds  
				stot   += ds 

		else:         # Lower surface
			swdr = self.switchdir(self.xl)
			stind,endind = self.findind( self.xl,xs,xe,swdr )
			for i in range(stind,endind): # 
				ds     = self.sl[i+1] - self.sl[i] 
                                avg    = (quant[i+1] + quant[i])/2.0 
				intval += avg*ds  
				stot   += ds 
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
		indout = -1 
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


	# integrate but include condition that will only integrate if values
	def res_int( self,xs,xe,quant,resval,thres,surf=0 ):
		# initialize integrated sum
		intval = 0.0 
		if surf == 0: # Upper surface 
			swdr = self.switchdir(self.xu) # see if dir switches
			stind,endind = self.findind( self.xl,xs,xe,swdr )
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

	
				

			










