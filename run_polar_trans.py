import numpy as np
import os
import subprocess
import time
from subprocess import Popen, PIPE


# airfoil is a string representing the coordinate file 
# xfoil will not let you change the forced transition location mid polar
def run_xfoil_trans( airfoil,Rey,mach,alpha,transu,transl,outname ):
    # Initiate subproccess  
    ps = subprocess.Popen(['xfoil'],
              stdin=subprocess.PIPE,
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


# function that reads file with alphas and transition locations for each
# angle, then runs xfoil with transition forced at those locations 

def run_polar_trans(airfoil,mach,Rey,transfile,outname):
    # assumes each row is alpha,lowerTrans,upperTrans 
    f = open(transfile) 
    lines = f.readlines()
    alphas,transU,transL = [],[],[]
    for line in lines:
        alphas.append( line.split()[0] )
        transU.append( line.split()[1] )
        transL.append( line.split()[2] )

    if os.path.exists( outname ):
        os.remove( outname ) 
    fd = os.open(outname, os.O_RDWR|os.O_CREAT )

    # need to go through and run each case individually so we can
    # manually set the transition locations, xfoil won't let you
    # change transition locations mid polar
    for i in range(len(alphas)):
        # just hardcode some arbitrary name as this is a temporary file
        if os.path.exists( 'temp_polar' ):
            os.remove( 'temp_polar' )

        run_xfoil_trans( airfoil,Rey,mach,alphas[i],
                     transU[i],transL[i],'temp_polar' )
        # need to force this to pause a little as the xfoil funtion takes a while
        time.sleep( 1.0 ) 

        # pull the last line from this file and save to actual output
        stdin,stdout = os.popen2( "tail -n 1 temp_polar" ) 
        stdin.close()
        line = stdout.readlines() 
        os.write( fd,line[0] ) 



airfoil = 's814.txt'
mach = 0.2
Rey = 2400000

# this will be the polar file output by this script
outname = 's814out'

# file that should have a rows of AoA, transU, transL 
transfile = 's814trans_140.txt' 

run_polar_trans(airfoil,mach,Rey,transfile,outname)




