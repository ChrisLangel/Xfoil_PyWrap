import numpy      as np
import subprocess as sp
#import os
from xfoil_func import *
from genNdata   import *
import shutil
import sys
import string
import time

        
airfoil = 'n63.txt'
# run clean version of the airfoil config and output data as .txt files
run_xfoil( airfoil,3.2e6,1.0,0.1,5.0 )
basename   = '3200000.0_A1.0' 
# gather all the info from text files and construct class 
classname  = const_class( basename,airfoil )

# need to run polar with the current  N_crit value
print classname.nu

