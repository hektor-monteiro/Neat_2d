#from ConfigNumParser import *
import numpy as np
from subprocess import call
from astropy.io import fits
import time
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

now = time.time() # used to time the code

##################################
# Program to call and run Neat
# !!!! perhaps should be turned to a function or module in the future

##################################
# Read in the image data cube and lambda vector

obj_dir = '/home/hmonteiro/Dropbox/work/devel/Neat_2d/neat-1.7/mz1/'
fits_file = 'mz1-emiss-map-cube.fits' 
hdulist = fits.open(obj_dir+fits_file)
scidata = hdulist[0].data

scidata = scidata[:,110:180,:] # use only a portion of the data cube
#scidata = scidata[:,140:141,:] # use only a portion of the data cube

fits_file = 'mz1-emiss-map-clambda.fits'
hdulist = fits.open(obj_dir+fits_file)
clambda = hdulist[0].data

##################################
# define indices of usefull data from output file

res_ind = [10,18,20,21,27,29,30,31,32,33,34,35,36,42,43,\
            44,45,46,47,48,49,50,51,52,53,54,55,61,62,63,\
            64,65,66,67,68,69,70,71,72,73,74,80,81,87,88,\
            89,90,96,97,98,99,100,101,102,103,108,109,110,\
            111,112,113,118,119,120,121,122,123,124,125,\
            126,127,128,129,130,131,132,133,134,135,136,\
            137,138,139,140,141,142,143,144,145,146,147,\
            148,149,150,151,152,153,154,155,160,163,\
            164,165,166,169,170,171,172,173,174,175,176,\
            177,178,179,182,183,184,185,186,187,188,189,\
            190,191,192,193,194,195,196,199,200,201,206,\
            207,208,209,210,211,216,217,218,219,220,221,\
            222]

res_descript = [] # description of data in each index
res_data = np.ndarray(shape=(147,scidata.shape[1],scidata.shape[2]), \
                      dtype=float)

##################################
# Starting here the loop to share in nodes
input = range(scidata.shape[1])
def run_neat(input):
##################################
# Loop through each pixel in data cube

for xpix in range(scidata.shape[1]):
    for ypix in range( scidata.shape[2]):    

##################################
# generate input text file from cube data

        for i in range(clambda.size):
            #print(clambda[i],scidata[i,xpix,ypix]/scidata[2,xpix,ypix])
            fl = scidata[:,xpix,ypix]/scidata[2,xpix,ypix]
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

###################################            
# loop through lines to get the calculated data
            cont = 0
            for i in range(0,nlines-1):
                aux = splitedlines[i].split()

                if i in res_ind:

                    res_descript.append(' '.join(aux[0:len(aux)-1]))
                    if (aux[len(aux)-1] != '--'):
                        res_data[cont,xpix,ypix] = float(aux[len(aux)-1])
                    else: 
                        res_data[cont,xpix,ypix] = -99.
#                    if cont == 0:
#                        print(res_data[cont,xpix,ypix])
                    cont = cont + 1

    sys.stdout.write("progress: %d%% \r" % (float(xpix)/scidata.shape[1]*100.))
    sys.stdout.flush()
########################################
# create final data cube fits file and lambda file

hduc = fits.PrimaryHDU(res_data)
hdulistc = fits.HDUList([hduc])
hdulistc.writeto('Neat-resCube.fits', clobber=True)


print "Finished calculations in", time.time()-now , "sec"
