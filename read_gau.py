#!/usr/bin/env python
"""
Created on 

@author: 
"""

import sys
import re
import math
#import numpy as np
#import matplotlib.pylab as plt
#import scipy.optimize as optimize
#import scipy.stats as stats
import os.path
import py_compile

from general import *
#from read_xyz import *

######################################################################
# FIND OPTIMIZATION
#def read_opt_gau(content):
#
#    OPT_GAU=0
#    for i in range(len(content)):
#        line = content[i]
#        s = re.search(r'Berny optimization.',line)
#        if s: 
#           OPT_GAU=1
#           break
#        else:
#           OPT_GAU=2
#    if OPT_GAU  == 1:
#        print("This is OPTIMIZATION")
#    elif OPT_GAU == 2:
#        print("This is SINGLE POINT")
#    return OPT_GAU
######################################################################
# FIND Type
def read_gau(content):
# Find typ of calculation
    GAU=0
    for i in range(len(content)):
        line = content[i]
        s = re.search(r'Number of optimizations in scan=',line)
        if s: 
           GAU=11
           break
        #find if this is a geometry optimization
        #any different type of opt ??
        s = re.search(r'Berny optimization.',line)
        if s: 
           GAU=1
           #find if this is a geometry optimization with scan (ModRed)
           for sline in content[i+1:]:
               ss = re.search(r'Number of optimizations in scan=',sline)
               if ss: 
                  GAU=11
                  break
           break
        #find if this calculation is TDDFT
        t = re.search(r'Excitation energies and oscillator strengths',line)
        if t: 
           x=line.split()
           GAU=2
           break
        #find if this calculation is NMR
        # any different typy ?
        n = re.search(r'GIAO',line)
        if n: 
           GAU=3
           break
        #if didnt find any above mention word the calculaition is Single Point
        #else:
        #   GAU=0
        # EPR ????
    if GAU  == 1:
        print("   This is a GEOMETRY OPTIMIZATION")
    elif GAU  == 11:
        print("   This is a GEOMETRY OPTIMIZATION with a PES SCAN")
    elif GAU  == 2:
        print("   This is a TD-DFT calculation")
    elif GAU  == 3:
        print("   This is a NMR calculation")
    elif GAU == 0:
        print("   This is a SINGLE POINT calculation")
    return GAU

#################################################################
# Did the program end correctly?
def read_end(content):        

    END=0
    for i in range(len(content)):
        line = content[i]
        #check if the program ended corectly        
        #for g16/g09
        o = re.search(r'Normal termination of Gaussian',line)
        if o: 
           END=1 #if "Normal termination of Gaussian" is found
           break
        else:
           END=2 #if "Normal termination ..." is not found and hence the program did end with an error
    if END == 1:
        print("   THE PROGRAM FINISHED CORRECTLY")
    if END == 2:
        print("   ERROR   ERROR   ERROR   ERROR") 
        print("   THE PROGRAM DID NOT END CORRECTLY")
    return END

###############################################################
# Check if the optimization is  completed
def read_opt_comp(content):        

#If the optimization is completed read new content2 
    content2=[]
    OC=0
    for i in range(len(content)):
        line = content[i]
        #Chceck if the optimization converged        
        #g16/g09
        o = re.search(r'Optimization completed.',line)
        if o: 
            OC=OC+1 #if optimization completed write everything after to content2 
        if OC == 1:
            content2.append(str(line))

    if OC == 1:
        print("   OPTIMIZATION COMPLETED")
    elif OC  == 0:
        print("   OPTIMIZATION NOT COMPLETED")
    return content2

#####################################################################
# Find data for g09/g16
# NAtoms : number of atoms
# Charge_gau : charge Charge_gau
# Mul_gau : multiplicity
# NA : alpha electrons
# NB : beta electrons
# OS : open shell (UHF OS=1, RHF OS=2, OS=0 ???)
# BF : number of Basis Functions
# PG : number of Primitive Gaussians
# CBF : number of Cartesian Basis Function
def get_data_gau(content):
    # we define NAtoms as global for reading xyz of inp and opt geoms (opt is the issue)
    global NAtoms
    NAtoms=read_NAtoms_gau(content)
    print("Number of atoms=",NAtoms)
    Charge_gau=read_Charge_gau(content)
    print("Charge=",Charge_gau)
    Mul_gau=read_Multiplicity_gau(content)
    print("Multiplicity=",Mul_gau)
    NA,NB=read_electrons(content)
    print("NA (alpha electrons)=",NA)
    print("NB (beta electrons)= ",NB)
    OS=read_OS(content)
    print("Open/Closed shell label (OS)=",OS)
    BF,PG,CBF=read_basis_function(content)
    print("number of Basis Functions=",BF)
    print("number of Primitive Gaussians=",PG)
    print("number of Cartesian Basis Function=",CBF)
    print()
    return NAtoms,Charge_gau,Mul_gau,NA,NB,OS,BF,PG,CBF


#####################################################################
# Find charge for g09/g16
def read_Charge_gau (content):

    Charge_gau=[] #vector 
    for i in range(len(content)):
        line = content[i]
        #g16/g09
        ch = re.search(r'Charge',line) 
        if ch: #if find charge
            x=line.split() #split the line with Charge
           # print(x)
            Charge_gau=int(x[2]) #write expreesion in the third place   
            break #end loop
    return Charge_gau
######################################################################
# Find Multiplicity for g09/g16
def read_Multiplicity_gau(content):

    Mul_gau=[] #Multiplicity in g16/g09
    for i in range(len(content)):
        line = content[i]
        #g16/g09
        m = re.search(r'Multiplicity',line)
        if m:
            x=line.split("=")
           # print(x)
            Mul_gau=int(x[2])
            break
    return Mul_gau
######################################################################
# Find the Number of Atoms in Gaussian
def read_NAtoms_gau(content):
    NAtoms=[] #Number of atoms in g09/g16
    for i in range(len(content)):
        line = content[i]
        #g16/g09
        s = re.search(r'NAtoms',line)
        if s:
            x=line.split()
         #   print(x)
            NAtoms=int(x[1])
            break
    return NAtoms

######################################################################
# Find Basis functions
def read_basis_function(content):
    
    BA=[] # Basis functions
    PG=[] # Primitive gaussians
    CBF=[] # Cartesian basis functions
    for i in range(len(content)):
        line = content[i]
        #g16/g09
        b = re.search(r'basis functions, ',line)
        if b:
            x=line.split()
#            print(x)
            BA=int(x[0])
            PG=int(x[3])
            CBF=int(x[6])
    return BA,PG,CBF
######################################################################
# Find Number of Basis
def read_Basis(content):
        
    NBasis=[] # Number of basis
    NBU=[]    # Number of used basis
    for i in range(len(content)):
        line = content[i]
        s = re.search(r'NBasis',line)
        if s:
            x=line.split()
            NBasis=int(x[1])
        s = re.search(r'NBsUse',line)
        if s:
            x=line.split()
            NBU=(x[1])
            break
    return NBasis,NBU
######################################################################
# Find the number of electrons
def read_electrons(content):
    
    EA=[] #number of alpha electrons
    EB=[] #number of beta electrons
    for i in range(len(content)):
        line = content[i]
        a = re.search(r'alpha electrons',line)
        b = re.search(r'beta electrons',line)
        if a:
            x=line.split()
            EA=int(x[0])
        if b:
            x=line.split()
            EB=int(x[3])
    return EA,EB
####################################################################
# Find Closed/Open shell
def read_OS (content): 
#check if the program is Open or Closed shell
    OS=0
    for i in range(len(content)):
        line = content[i]
        o = re.search(r'UHF open shell SCF',line)
        if o:
           print('The system is OPEN SHELL')
           OS=1  
           break
        c = re.search(r'Closed shell SCF',line)
        if c:
           print('The system is CLOSED SHELL')
           OS=2
           break
    if OS == 0:
       print("Possibly an RESTRICTED OPEN SYSTEM or GCHF - not recognized yet! Sorry :(")
    return OS

######################################################################
# FIND THE ENERGY  
def read_energy(content,GAU):
#its running iteration in Single Point    
    IT="" # comment Iteration
    num=[] # number of iteration
    EE=[]  # Energy 
    for i in range(len(content)):
        line = content[i]
        if GAU ==0:
            s = re.search(r'Iteration',line)
            if s:
                x=line.split()
                print(x)
                IT=x[0]
                num.append(int(x[1]))
                #EE for Single Point
                EE.append(float(x[3]))
        else:
            break
    return IT,num,EE

######################################################################
# FIND  Excited states
def read_TDDFT(content,GAU):
    
    lev=[]  # wavelength in eV
    lnm=[]  # wavelength in nm
    com="" #  only an intermediate step to split oscillator strengths
    f=[]   # oscillator strengths
    for i in range(len(content)):
        line = content[i]
        if GAU ==2:
            #TDDFT for g16/g09
            s = re.search(r'Excited State',line)
            if s:
                x=line.split()
                lev.append(float(x[4]))
                lnm.append(float(x[6]))
                # split oscillator strengths
                com=x[8]
                y=com.split("=") # = is the separator for spliting
                f.append(float(y[1])) # print only the actual value of oscillator strengths
    # printing output            
    print('--------------------------------------------------------------------------')
    print('                     E X C I T E D   S T A T E S                          ')
    print('--------------------------------------------------------------------------')
    # we will avoid using the special character \u03BB for lambda
    #print('\u03BB / ev','\t\t','\u03BB / nm','\t','oscillator strengths')
    print('lambda / ev','\t','lambda / nm','\t','oscillator strengths')
    for i in range(len(lnm)):
        print('{:7.3f}'.format(lev[i]),'\t','{:7.3f}'.format(lnm[i]),'\t','{:8.4f}'.format(f[i]))

    # we can get rid of the com variable
    return lev,lnm,com,f

######################################################################
# lets write the excited states into a file 
# we just give beack the content2 str variable !!!
def give_TDDFT_content(lev,lnm,f):
    print("START give_TDDFT_content")
    content2=""
    content2 ='#--------------------------------------------------------------------------'+"\n"
    content2+='#                     E X C I T E D   S T A T E S                          '+"\n"
    content2+='#--------------------------------------------------------------------------'+"\n"
    #content2+=('lambda / ev \t lambda / nm \t oscillator strengths \n')
    content2+=('i,lambda / ev, lambda / nm, oscillator strengths \n')
    for i,ilev in enumerate(lev):
    #    content2+=('{:7.3f}'.format(lev[i]),'\t','{:7.3f}'.format(lnm[i]),'\t','{:7.3f}'.format(f[i]))
    #    content2+=("%7.3f \t %7.3f \t %7.3f \n" % (lev[i],lnm[i],f[i]))
        content2+=("%4i, %7.3f, %7.3f, %8.4f \n" % (i+1,lev[i],lnm[i],f[i]))
    
    content2+='#--------------------------------------------------------------------------'+"\n"
    
    #print(content2)
    print("END give_TDDFT_content")

    return(content2)
        
######################################################################
# lets write the UV-vis like spectrum 
# we just give beack the content2 str variable !!!
def give_TDDFT_lnm_spectrum(lnm,f):
    content2=""
    content2="# lambda / nm, UV-vis spectrum / arbitrary units \n"
    content2="\u03BB [nm], I [-] \n"

    lnm2,f2=get_TDDFT_lnm_spectrum(lnm,f)
    for i,ilnm2 in enumerate(lnm2):
        content2+=("%7.1f , %12.3f \n" % (lnm2[i],f2[i]))

    return(content2)

######################################################################
# lets calculate the UV-vis like spectrum from known transitions and osc. strengths
def get_TDDFT_lnm_spectrum(lnm,f):
    lnm2=[]
    f2=[]

    min_lnm=round(lnm[-1]-50,0)
    max_lnm=round(lnm[0]+400,0)
    #print(type(min_lmn)) # it is a float!
    print("min_lnm=",min_lnm)
    print("max_lnm=",max_lnm)
    
    val_lnm=min_lnm
    while val_lnm <= max_lnm:
          lnm2.append(val_lnm)
          f2.append(0.0)
          val_lnm=val_lnm+1.0
    
    # http://gaussian.com/uvvisplot/
    k=1.3062974E8
    #k=1.0
    sigma=1/3099.6 #nm ~ 0.4 eV
    #sigma=sigma/10.0 #nm ~ 0.04 eV
    for i,ilnm in enumerate(lnm):
        # http://gaussian.com/uvvisplot/
        # k= 1.3062974E8
        # sigma=0.4 eV
        # ei(nu)=k*f[i]/sigma * exp( - (nu-nu[i]) / sigma  )

        # sigmal=1/3099.6 nm
        # ei(lambda)=k * f/(1.0E7/3099.6) * exp( -(1/lambda-1/lambda[i])**2/(1/3099.6)) 

        fi=f[i]
        if fi < 0.00001:
           fi=1.0E-6
        li=ilnm
        print(li,fi)
        for j,jlnm2 in enumerate(lnm2):
            l=jlnm2 #lambda
            f2l=k*fi/(1.0E7/3099.6) * math.exp( -(1.0/l-1.0/li)**2/(1/3099.6)**2)
            f2[j]=f2[j]+f2l

    return(lnm2,f2)

#######################################################################
def main():
    print("This is a py file for g09/g16 file data reading.")

#######################################################################
# to run main in this py file
if __name__ == "__main__":
   main()


