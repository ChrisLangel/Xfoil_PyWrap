# -*- coding: utf-8 -*-
 
import subprocess as sp
#import os
import shutil
import sys
import string
import time

# Name of coordinate file to load
coords = 's814.dat' 

"""
class Popen(args, bufsize=0, executable=None,
            stdin=None, stdout=None, stderr=None,
            preexec_fn=None, close_fds=False, shell=False,
            cwd=None, env=None, universal_newlines=False,
            startupinfo=None, creationflags=0):
"""

# Initiate subproccess  
ps = sp.Popen(['xfoil'],
              stdin=sp.PIPE,
              stdout=None,
              stderr=None)

# define function to give commands to xfoil from python 
def issueCmd(cmd,echo=True):
    ps.stdin.write(cmd+'\n')
    if echo:
        print cmd

# load coordinates and enter OPER mode
issueCmd( ''.join(['load ', coords]) ) 
issueCmd( 'oper' ) 
# Set new iteration limit
issueCmd( 'iter 40' ) 

# Switching over to viscous mode requires Reynolds number input so declare an array of Re's here
Reys = [ 1.6e6, 2.4e6, 3.2e6 ]  

issueCmd( 'visc' )
# Enter Reynolds number   r>
issueCmd( str(Reys[0]) ) 
issueCmd( 'm 0.2' )

# set the N_crit value
issueCmd( 'vpar' )
issueCmd( 'N 6.0' )
issueCmd( ' ' )


for rey in Reys:
	issueCmd( ''.join(['R ', str(rey)]) ) 
        # Run a few intermediate angles to make sure we converge when starting new polar
        issueCmd('ALFA -4.0' )
        issueCmd( '!' ) 
        issueCmd('ALFA -8.0' )
        issueCmd( '!' ) 
	# run a polar at this Rey
        for aoa in [-10+(i*.5) for i in range(40)]:
        	 issueCmd( 'ALFA %7.4f' % (aoa,) ) 
                 issueCmd( 'vplo' )
                 issueCmd( 'n' ) 
                 time.sleep( 0.2 ) 
                 # create signature for file 
                 issueCmd( ''.join(['dump ',str(rey),'_A',str(aoa),'.nc']) )   
		 time.sleep( 0.2 ) 
		 issueCmd( 'RT' )
		 time.sleep( 0.2 ) 
                 issueCmd( ''.join(['dump ',str(rey),'_A',str(aoa),'.rt']) )   
		 time.sleep( 0.2 ) 
		 issueCmd( 'CF' )
		 time.sleep( 0.2 ) 
                 issueCmd( ''.join(['dump ',str(rey),'_A',str(aoa),'.cf']) )   
		 time.sleep( 0.2 ) 
		 issueCmd( 'UE' )
		 time.sleep( 0.2 ) 
                 issueCmd( ''.join(['dump ',str(rey),'_A',str(aoa),'.ue']) )   
		 time.sleep( 0.2 ) 
		 issueCmd( 'DT' )
		 time.sleep( 0.2 ) 
                 issueCmd( ''.join(['dump ',str(rey),'_A',str(aoa),'.dt']) )   
		 time.sleep( 0.2 ) 
		 issueCmd( 'DB' )
		 time.sleep( 0.2 ) 
                 issueCmd( ''.join(['dump ',str(rey),'_A',str(aoa),'.db']) )   
		 time.sleep( 0.2 ) 
                 issueCmd( ' ' )
		 issueCmd( 'CPWR' )
                 issueCmd( ''.join([str(rey),'_A',str(aoa),'.cp']) )
		 time.sleep( 0.2 ) 

		 
issueCmd( ' ' ) 
issueCmd( ' ' ) 
issueCmd( 'quit' ) 
                 
    
				



