import NXdata
from NXdata import *
import matplotlib.pyplot as plt

xl   = R1600000_0_A5X.xl
xu   = R1600000_0_A5X.xu
Dcpu = R1600000_0_A5X.Dcpu
cpu  = R1600000_0_A5X.cpu

for i in range(len(cpu)):
	cpu[i] = -1.0*cpu[i]

for i in range(len(xu)):
	print xu[i],Dcpu[i] 

for i in range(25):
	print R1600000_0_A5X.intquant( 0.02, 0.02*(i+1), Dcpu, 0 ),0.02*(i+1) 

#plt.plot(xu, Dcpu) 
#plt.show()


# A way to convert a string into a fully accesible class !!!
class_from_string = globals()[ 'classname' ] 

# If one needs to access some attribute of a class, 
xu  = getattr( ex_class, 'xu' )

# foo now becomes the function that was part of the ex_class 
foo = getattr( ex_class, 'some_function' ) 

 





