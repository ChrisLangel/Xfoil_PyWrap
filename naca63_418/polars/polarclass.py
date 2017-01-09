#!/usr/bin/python

class polar:
	'AoA,cl,cd,trans - arrays corresponding to label'
	'c_o_r - clean or rough (input 1 for rough 0 for clean)' 
	testct = 0
	def __init__(self,AoA,cl,cd,c_o_r,AoAt,trans,height,den):
		self.AoA  = AoA
		self.AoAt = AoAt 
		self.cl   = cl
		self.cd   = cd
		self.trans = trans
		if c_o_r == 1:
			self.height = height
			self.den    = den
		self.c_o_r = c_o_r
		polar.testct += 1 
		self.axisset,self.xlabel,self.ylabel = 0,0,0
	def listcl(self):
		return self.cl
		print self.cl 
	def listcd(self):
		return self.cd
		print self.cd
	

# -----------  Functions Related to plotting polars --------------------
	def setaxis(self,xlim,ylim):
		self.axisset = 1 
		self.xlim = xlim
		self.ylim = ylim 

	def setylabel(self,ylabel):
		self.ylabel = 1
		self.ylabel = ylabel

	def setyxlabel(self,ylabel):
		self.xlabel = 1
		self.xlabel = xlabel 

	def plotpolar(self,*args,**kwargs):
		import matplotlib.pyplot as plt
		# Make sure to use shorter array as length
		if len(self.cl) > len(self.cd): 
			tot = len(self.cd)
		else:
			tot = len(self.cl)
		plt.plot(self.cl[0:tot],self.cd[0:tot],*args,**kwargs) 
		if self.axisset:
			plt.xlim(self.xlim)
			plt.ylim(self.ylim) 
		if self.xlabel:
			plt.xlabel(self.xlabel)
		else: 
			plt.xlabel('$ C_l $',fontsize=24)
		if self.ylabel:
			plt.ylabel(self.ylabel)
		else: 
			plt.ylabel('$ C_d $',fontsize=24)
		
	
				
	def plotclalfa(self,*args,**kwargs):
		import matplotlib.pyplot as plt
		# Make sure to use shorter array as length
		if len(self.cl) > len(self.AoA): 
			tot = len(self.AoA)
		else:
			tot = len(self.cl)
		plt.plot(self.AoA[0:tot],self.cl[0:tot],*args,**kwargs) 
		if self.axisset:
			plt.xlim(self.xlim)
			plt.ylim(self.ylim) 
		if self.xlabel:
			plt.xlabel(self.xlabel)
		if self.ylabel:
			plt.ylabel(self.ylabel)
	

	def plottrans(self,*args,**kwargs):
		import matplotlib.pyplot as plt
		# Make sure to use shorter array as length
		if len(self.trans) > len(self.AoAt): 
			tot = len(self.AoAt)
		else:
			tot = len(self.cl)
		plt.plot(self.trans[0:tot],self.AoAt[0:tot],*args,**kwargs) 
		if self.axisset:
			plt.xlim(self.xlim)
			plt.ylim(self.ylim) 
		if self.xlabel:
			plt.xlabel(self.xlabel)
		if self.ylabel:
			plt.ylabel(self.ylabel)

	def show(self):
		import matplotlib.pyplot as plt
		plt.show() 

	def legend(self,*args,**kwargs):
		import matplotlib.pyplot as plt
		plt.legend(*args,**kwargs) 




		
		
