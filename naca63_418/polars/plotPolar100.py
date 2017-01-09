#!/usr/bin/env python

# -------------------------------  Header ----------------------------------
import pylab
from pylab import figure,plot,matplotlib
from matplotlib import pyplot as plt
import numpy as np

import polardata
from polardata import *
from n63polardata import *

matplotlib.rcParams.update({'font.size': 16})
matplotlib.rc('legend',**{'fontsize': 14})


#------------------------------ Default Figure Size -----------------------

fig = figure(num=None, figsize=(14,6), dpi=80 )
fig.subplots_adjust(bottom=0.12)
fig.subplots_adjust(top=0.91)
fig.subplots_adjust(right=0.96)
fig.subplots_adjust(left=0.1)
fig.subplots_adjust(wspace=0.14)
# -------------------------------------------------------------------------

# Plot commands
ax = fig.add_subplot(131)
N6E1Eclean_Re_1_6E.plotpolar('ko',markersize=10, linewidth=2)
N6E3E100_15_Re_1_6E.plotpolar('o',color=[0.0,0.4,0.0], mec=[0.0,0.4,0.0],markersize=10, linewidth=2)
X_n63polar1_6_clean.plotpolar('--s',color=[0.0,0.2,0.2],mec=[0.0,0.2,0.2],mfc='none',mew=2,markersize=10, linewidth=2)
X_n63polar1_6_140.plotpolar('--s',color=[1.0,0.0,0.3],mec=[1.0,0.0,0.3],markersize=10, linewidth=2)


plt.ylim([0,0.025])
plt.xlim([-0.5,1.5])
plt.title('$ Re_c =  1.6 \\times 10^6$')
plt.xlabel('$C_l$')
plt.ylabel('$C_d$')
plt.grid()
labels = ['Clean (exp)', 'Rough (exp)', 'Clean (XFOIL)', 'Rough (XFOIL)']
plt.legend(labels,loc=2,numpoints=1)


ax = fig.add_subplot(132)
N6E3Eclean_Re_2_4E.plotpolar('ko',markersize=10, linewidth=2)
N6E3E100_15_Re_2_4E.plotpolar('o',color=[0.0,0.4,0.0], mec=[0.0,0.4,0.0], markersize=10, linewidth=2)
X_n63polar2_4_clean.plotpolar('--s',color=[0.0,0.2,0.2],mec=[0.0,0.2,0.2],mfc='none',mew=2,markersize=10, linewidth=2)
X_n63polar2_4_140.plotpolar('--s',color=[1.0,0.0,0.3],mec=[1.0,0.0,0.3],markersize=10, linewidth=2)

ax.set_yticklabels([])
plt.ylim([0,0.025])
plt.xlim([-0.5,1.5])
plt.title('$ Re_c =  2.4 \\times 10^6$')
plt.xlabel('$C_l$')
plt.ylabel('')
plt.grid()

ax = fig.add_subplot(133)
N6E3Eclean_Re_3_2E.plotpolar('ko',markersize=10, linewidth=2)
N6E3E100_15_Re_3_2E.plotpolar('o',color=[0.0,0.4,0.0], mec=[0.0,0.4,0.0], markersize=10, linewidth=2)
X_n63polar3_2_clean.plotpolar('--s',color=[0.0,0.2,0.2],mec=[0.0,0.2,0.2],mfc='none',mew=2,markersize=10, linewidth=2)
X_n63polar3_2_140.plotpolar('--s',color=[1.0,0.0,0.3],mec=[1.0,0.0,0.3],markersize=10, linewidth=2)

ax.set_yticklabels([])
plt.ylim([0,0.025])
plt.xlim([-0.5,1.5])
plt.title('$ Re_c =  3.2 \\times 10^6$')
plt.xlabel('$C_l$')
plt.ylabel('')
plt.grid()

plt.show()
