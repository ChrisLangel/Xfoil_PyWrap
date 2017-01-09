import numpy as np
import subprocess as sp
#import os
import time

        
# airfoil is a string representing the coordinate file 
# xfoil will not let you change the forced transition location mid polar
def run_xfoil_trans( airfoil,Rey,mach,alpha,transu,transl,outname ):
    # Initiate subproccess  
    ps = sp.Popen(['xfoil'],
              stdin=sp.PIPE,
              stdout=None,
              stderr=None)
    # define function to give commands to xfoil 
    def issueCmd(cmd,echo=True):
        ps.stdin.write(cmd+'\n')
        if echo: print cmd
        
    # load coordinates and enter OPER mode
    issueCmd( ''.join(['load ', airfoil]) ) 
    issueCmd( 'oper' ) 
    # Set new iteration limit
    issueCmd( 'iter 40' ) 
    issueCmd( 'visc' )
    # Enter Reynolds number   r>
    issueCmd( str(Rey) )
    # mach number 
    issueCmd( ''.join([ 'm ', str(mach)  ]) )
    
    # go to boundary layer parameter menu and set transition locations
    issueCmd( 'VPAR' )
    issueCmd( 'XTR' )
    issueCmd( str(transu) )
    issueCmd( str(transl) )
    issueCmd( ' ' ) 
    
    issueCmd( 'Pacc' )
    issueCmd( ' ' )
    issueCmd( ' ' )
    issueCmd( ''.join([ 'ALFA ', str(alpha) ]) )
    time.sleep( 0.2 )

    issueCmd( 'pwrt' )
    issueCmd( outname )
    issueCmd( 'y' ) 
    issueCmd( ' ' ) 
    issueCmd( ' ' ) 
    issueCmd( 'quit' ) 
    

    

