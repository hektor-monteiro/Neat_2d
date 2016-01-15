#from ConfigNumParser import *
import numpy as np
from subprocess import call
from astropy.io import fits

##################################
# Program to call and run Neat
# !!!! should be turn to a function or module in the future

##################################
# Read in the image data cube and lambda vector
obj_dir = '/home/hmonteiro/Dropbox/work/devel/Neat_2d/neat-1.7/mz1/'
fits_file = 'mz1-emiss-map-cube.fits' 
hdulist = fits.open(obj_dir+fits_file)
scidata = hdulist[0].data

fits_file = 'mz1-emiss-map-clambda.fits'
hdulist = fits.open(obj_dir+fits_file)
clambda = hdulist[0].data

##################################
# generate input text file from cube data

for i in range(clambda.size):
    print(clambda[i],scidata[i,150,10]/scidata[2,150,10])

fl = scidata[:,150,10]/scidata[2,150,10]
aux=np.array([clambda,fl,fl*0.02])

np.savetxt(obj_dir+'temp.out', aux.transpose(), \
           fmt='%f', newline='\n')   # use exponential notation

##################################
# Run Neat on the generated input file

neat_dir = '/home/hmonteiro/Dropbox/work/devel/Neat_2d/neat-1.7/'
input_file = obj_dir+'temp.out'
flags = " "

call('./neat -i'+' '+input_file+' '+flags+'>trash.out', shell=True)


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

    if len(aux) > 1:
        print(' '.join(aux[0:len(aux)-1]),aux[len(aux)-1])
        

