import numpy as np
import matplotlib.pyplot as plt
from pylab import loadtxt
import os

# Import all the data
from transdict_s814 import *
from SXdata        import *

# Import correlation functions
from cor_funcs import *

# load parameters from file
corPms = loadtxt('corParams')
ReyPwr = float(corPms[0])
intPwr = float(corPms[1])

# example key syntax               - '3_2_140_15_2_0'
# example name of class from xfoil - 'R1600000_0_A5X'
#
if __name__ == '__main__':
    if os.path.exists( 'cor_data.txt' ):
    	os.remove( 'cor_data.txt' )

    fd = os.open('cor_data.txt', os.O_RDWR|os.O_CREAT )

    rtcrt,ncrit,alphs,dist,labels,keys = [],[],[],[],[],[]
    Reystr = [ '2_4','3_2' ]
    rhts   = [ '140' ]
    dens   = [ '03' ]
    pq,crit = [],[]
    classes, exptrans = [],[]
    for den in dens:
      #pq,crit = [],[]
      for rstr in Reystr:
        rnum    = ''.join([list(rstr)[0],list(rstr)[2]])
        for rht in rhts:
            # need to do some sort of scaling to account for lower densities
            if   den == '03' : scale = 0.9
            elif den == '06' : scale = 0.92
            elif den == '09' : scale = 0.94
            elif den == '15' : scale = 1.0
            k_s = float(rht)*1.0e-6*scale
            # automate by generating the substring on the fly
            # subst   = '2_4_140_03_'
            subst   = ''.join(['U_',rstr, '_', rht, '_', den, '_' ])
            print subst
            curkeys = get_key_list( subst,transdict )
            print curkeys
            for key in curkeys:
                err     = False
                aoastr  = ''.join( get_str_diff( key,subst ))
                print aoastr
                classtr = ''.join( ['R',rnum,'00000_0_A',aoastr,'X' ] )
                try: thisclass = globals()[ classtr ]
                except: err = True
                if not err:
                      classes.append( classtr )
                      exptrans.append( float( transdict[key][0] )  )
                      # extract the data from class for this configuration
                      xu,su,n,rt,Dcp,cf,K,mut,dstr,mom,thw = extract_vars( thisclass )
            		# compute the correlation function
                      quant = comp_quant( k_s,K,mut,thw,dstr,mom )
                      quant2 = []
                      # Add some Reynolds number scaling to the computed function
                      for q in quant:
                          quant2.append( q*(float(rnum)**ReyPwr) )
                          #quant2.append( q )
                      #
                      foo   = getattr( thisclass, 'intquant' )
                      trans = float( transdict[key][0] )
                      ind   = near_ind( xu,trans )
                      ncrit.append( 1.0 - (n[-1]  -  n[ind])/n[-1] )
                      rtcrt.append( 1.0 - (rt[-1] - rt[ind])/rt[-1] )

                      crit.append( rt[ind]/rt[-1] )
                      dist.append( (foo(0.12,0.02,np.array(quant2)))**intPwr )
                      pq.append(   (foo(0.12,0.02,np.array(quant2)))**intPwr )
                      keys.append( key )
                      alphs.append( aoastr )
      leg    = ''.join([rnum,'_',rht])
      labels = labels + [leg]
      plt.plot( pq, crit,'*',markersize=10 )
    for i in range(len( ncrit )):
        wrtstr = ''.join([str(dist[i]),'   ',str(ncrit[i]),'   ',str(keys[i]),'\n'])
        os.write(fd,wrtstr)
    print pq, crit
    thresh = bin_arrays( pq,crit )
    print thresh
    # generate a linear best fit line
    # now we are looking at finding the line that is after the flat line
    downslope = []
    downdist  = []
    for i in range(len(crit)):
        if dist[i] > thresh:
            downdist.append( dist[i] )
            downslope.append( crit[i] )

    m,c  = np.polyfit( downdist,downslope,1 )
    print m,c
    line = []
    for d in dist:
    	line.append( d*m + c )

    plt.plot( dist,line  )
    # plt.legend( labels )
    plt.xlabel( '$\\int \ \  R_{\\Lambda} \ ds$' )
    plt.ylabel( '$\\frac{Re_{\\theta t, rough}}{Re_{\\theta t}}  $', fontsize=22 )
    plt.ylim( [0,1.2 ] )
    #plt.xlim( [0,2000] )
    plt.show()
    print np.corrcoef( downdist,downslope )
