#from ConfigNumParser import *
import numpy as np
from subprocess import call

##################################
# Program to call and run Neat
# !!!! should be turn to a function or module in the future

dir = '/home/hmonteiro/Dropbox/work/devel/Neat_2d/neat-1.7/'
input_file = dir+'examples/ngc6543.dat'
flags = " "

call('./neat -i'+' '+input_file+' '+flags, shell=True)


###################################
# Parse output file

f=open(input_file+'_results',"r")
txt=f.read() #all text is in txt
f.close()

splitedlines = txt.splitlines() #split file into an array of lines

nlines = len(splitedlines) # get the number of lines in the file

# loop through lines to get the calculated data

for i in range(0,nlines-1):
    aux = splitedlines[i].split()
    print(aux)
    if len(aux) > 1:
        print(' '.join(aux[0:len(aux)-1]),aux[len(aux)-1])
        


