# Program to call and run Neat
# !!!! should be turn to a function or module in the future

from subprocess import call

dir = '/home/hmonteiro/Dropbox/work/devel/Neat_2d/neat-1.7/'
input_file = dir+"examples/ngc6543.dat"
flags = " "

call('neat -i'+' '+input_file+' '+flags, shell=True)

#pid = Popen(["/bin/mycmd", "myarg"]).pid
