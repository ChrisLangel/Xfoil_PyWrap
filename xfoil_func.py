import numpy as np
import subprocess as sp
#import os
import shutil
import sys
import string
import time

        
# airfoil is a string representing the coordinate file 
def run_xfoil( airfoil,Rey,alpha,mach,ncrit ):
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
    issueCmd( ''.join([ 'm', str(mach)  ]) ) 
    issueCmd( 'VPAR' )
    issueCmd( ''.join([ 'N', str(ncrit) ]) )
    issueCmd( ' ' ) 
    issueCmd( ''.join([ 'ALFA', str(alpha) ]) )
    # go into the boundary layer plotting part of XFOIL     
    issueCmd( 'vplo' )        
    cmds = [ 'n', 'RT', 'CF', 'UE', 'DT', 'DB' ]
    exts = ['.nc', '.rt', '.cf', '.ue', '.dt','.db' ]
    for i in range(len(cmds)):
        issueCmd( cmds[i] )
        time.sleep( 0.2 )
        issueCmd( ''.join(['dump ',str(Rey),'_A',str(alpha), exts[i] ])  )
    time.sleep( 0.2 )    
    issueCmd( ' ' )
    issueCmd( 'CPWR' )
    issueCmd( ''.join([str(Rey),'_A',str(alpha),'.cp']) )
    time.sleep( 0.2 ) 
    issueCmd( ' ' ) 
    issueCmd( ' ' ) 
    issueCmd( 'quit' ) 
    

    

