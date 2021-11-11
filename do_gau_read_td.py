#!/usr/bin/env python3
"""
Created on 11. Nov. 2021

@author: Lukas Bucinsky FCHPT STU Bratislava Slovakia. 
"""

# python settings
import sys
import re
import os.path

# le_pychemy_go: ADJUST THE PYTHONPATH
#export PYTHONPATH=$le_pychemy_go_DIR
from read_gau import *

# additional stuff for plt 
import matplotlib.pyplot as plt
#from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from scipy import stats
#import sys
#import os.path



#######################################################################
def main():
    print("This is a py file for g09/g16 file data reading.")
    print()

    # first we check whether we get an argument ifile,
    # where ifile is the input out file
    try:
        ifile = sys.argv[1]
    #    ifile2 = sys.argv[2]
    except:
        print('We want an gaussian output file')
        print('Program usage:')
        print(sys.argv[0],'file.out')
        sys.exit()
    
    fname0=os.path.splitext(ifile)[0]
    fname1=os.path.splitext(ifile)[1]
    
    # get the content
    # here we read the ifile= sys.argv[1]
    content=open_read_file(ifile)
    
    # check the job type
    GAU=read_gau(content)
    print("GAU=",GAU)
    print()
    
    # check the normal termination of gauusian
    END=read_end(content)
    #print(END)

    # get info : NAtoms,Charge_gau,Mul_gau,NA,NB,OS,BF,PG,CBF
    # see read_gau.get_data_gau
    print()
    get_data_gau(content)
    
    # read TDDFT
    lev,lnm,com,f = read_TDDFT(content,GAU)
    # write tddft excitations lev,lnm,f into a file
    content2=give_TDDFT_content(lev,lnm,f)
    #print(content2)
    tfile=fname0+".td.txt"
    write_content_file(tfile,content2)

    # calculate the spectra (lnm is used)
    content2=give_TDDFT_lnm_spectrum(lnm,f)
    #print(content2)
    sfile=fname0+".td.dat"
    write_content_file(sfile,content2)

    # plotting the spectrum in ofiles
    # read transitions (colums are to be plotted)
    tdf = pd.read_csv(tfile, sep=',',comment="#")
    tdata = tdf.values.transpose()
    # read spetrum
    sdf = pd.read_csv(sfile, sep=',')
    sdata = sdf.values.transpose()

    xs=sdata[0]
    ys=sdata[1]
    
    #normalization constant
    c_norm = max(ys)
    y_norm = max(tdata[3])/0.5
    #y_norm=0.01

    xtbar=tdata[2]
    ytbar=tdata[3]*c_norm/y_norm

    #matplotlib.rcParams.update({'font.size': 16})
    plt.rcParams.update({'font.size': 14})
    #plt.tight_layout(pad=1.5, w_pad=1.5, h_pad=1.5) 
    plt.rcParams.update({'figure.autolayout': True})
    
    plt.figure(figsize=(5.5, 5.5))
    #plt.plot( xs, ys, 'bo')
    plt.plot( xs, ys)
    w=3.0
    plt.bar(xtbar,ytbar,width=w,color='black')
    
    # has to be adjusted manually
    red_bar=[9,60,83]
    
    for rb in red_bar:
        plt.bar(xtbar[rb-1],ytbar[rb-1],width=w,color='red')
    
    plt.xlabel(sdf.columns[0])
    plt.ylabel(sdf.columns[1])

    png_name=str(fname0)+"_2.png"
    eps_name=str(fname0)+"_2.eps"

    plt.savefig(png_name, dpi= 300)
    plt.savefig(eps_name, format='eps')
    plt.close()



#######################################################################
# to run main in this py file
if __name__ == "__main__":
    main()


