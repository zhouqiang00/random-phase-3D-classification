#!/usr/bin/env python
import os,sys
import re
import glob
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser
prog_name=os.path.basename(sys.argv[0])
usage="""
{prog} options
plot the class number distribution of particles.
Written by Zhou Qiang @ Yan lab, School of Medicine, Tsinghua University.
""".format(prog=prog_name)

optParser= OptionParser(usage)
optParser.add_option("-i","--inputstar",action="store",type="str",dest="inputstar",default="",help="One data.star file from a iteration cycle from which all data.star files will be analyzed. [default: %default]")
optParser.add_option("-d","--data_array",action="store",type="str",dest="data_array",default="",help="File of data array storing particles class number distribution. If this file exists, load it, other than dump data array into a file of this name. [default: %default]")
optParser.add_option("--show_fig",action="store_true",dest="show_fig",default=False,help="Show figures. [default: %default]")
optParser.add_option("--save_class_dis_particles",action="store",type="str",dest="save_class_dis_particles",default="",help="The name of the figure showing the distribution of the times belonging to the randomized class of the particles. [default: %default]")
optParser.add_option("--save_class_dis_iteration",action="store",type="str",dest="save_class_dis_iteration",default="",help="The figure name of the fraction of the randomized class in each iteration. [default: %default]")
optParser.add_option("-o","--outputstar",action="store",type="str",dest="outputstar",default="",help="Output relion datastar with particles appearing in phase-randomed class not larger than the threshold. [default: %default]")
optParser.add_option("-t","--threshold",action="store",type="float",dest="threshold",default= 3.,help="Threshold of times particles appear in the phase-randomed class. Particles with smaller than or equal to this value will be reserved. [default: %default]")
optParser.add_option("--plot_lower_times",action="store",type="float",dest="plot_lower_times",default= 0.,help="Lower bad times to plot. [default: %default]")
optParser.add_option("--start_iter",action="store",type="int",dest="start_iter",default= 0,help="Starting number of iteration to count the times in phase-randomized class, counted from 1. [default: %default]")
optParser.add_option("--end_iter",action="store",type="int",dest="end_iter",default= 0,help="Ending number of iteration to count the times in phase-randomized class, counted from 1. [default: %default]")
optParser.add_option("-v","--verbose",action="store_true",dest="verbose",default= False,help="Print more information when verbose. [default: %default]")
(options,args)=optParser.parse_args()

if not options.inputstar:
	print "Please input a relion data.star file."
	exit(1)

patiter=re.compile(r"_it\d{3,3}_")
alldatas=patiter.sub("_it???_",options.inputstar)
all_stars=glob.glob(alldatas)
all_stars.sort()
# do not take iter 0 into account
patiter0=re.compile(r".*_it000_.*")
if patiter0.match(all_stars[0]):
	all_stars=all_stars[1:]
nr_iters=len(all_stars)
# find the number of particles in a star file
# 
f1=open(all_stars[0])
n=0
i_classnumber=0
for line in f1:
	ln_s=line.split()
	if (len(ln_s) > 3):
		n += 1
	else:
		if line.startswith("_rlnClassNumber"):
			i_classnumber = int(line.split("#")[1]) - 1
f1.close()
nr_ptcls=n

# create zero array of class number
# check and load previous data
# particle in axis 0
# iteration in axis 1
if os.path.isfile(options.data_array):
	array_clsnumber=np.load(options.data_array)
else:
	array_clsnumber = np.zeros((nr_ptcls,nr_iters), dtype=np.int)
	# fill array 
	i=0
	for star in all_stars:
		j = 0
		f=open(star)
		for line in f:
			ln_s = line.split()
			if (len(ln_s) > 3):
				if int(ln_s[i_classnumber]) >= 2:
                                        myclassnumber=1
                                else:
                                        myclassnumber=0
				array_clsnumber.itemset((j,i),myclassnumber)
				j += 1
		f.close()
		i += 1
	if options.data_array:
		array_clsnumber.dump(options.data_array)

# Section according to star iter or end iter
if options.start_iter >=  1 or options.end_iter >= 1 :
	if options.start_iter >=  1 and options.end_iter <= 0 :
		array_clsnumber = array_clsnumber[:,options.start_iter - 1:]
	if options.start_iter <=  0 and options.end_iter >= 1 :
		array_clsnumber = array_clsnumber[:,:options.end_iter]
	if options.start_iter >=  1 and options.end_iter >= 1 :
		array_clsnumber = array_clsnumber[:,options.start_iter - 1:options.end_iter]
	nr_iters=array_clsnumber.shape[1]

# find the particles class distribution
ptcls_numberInRandomRef = array_clsnumber.mean(axis = 1) * nr_iters
RandomRef_inEachIteration = array_clsnumber.mean(axis= 0 ) 
#print RandomRef_inEachIteration

# plot class distribution of particles
# numberInRam_frac is percentage of each group
# numberInRam is boarder value of groups
plt.clf()
if options.plot_lower_times == 0. :
	(numberInRam_frac,numbersInRam,dummy)=plt.hist(ptcls_numberInRandomRef,bins=nr_iters,range=(options.plot_lower_times,nr_iters),normed = 1)
else:
	(numberInRam_frac,numbersInRam,dummy)=plt.hist(ptcls_numberInRandomRef,bins=nr_iters,range=(options.plot_lower_times,nr_iters))
plt.xlabel(r"# of times in phase-randomized class",fontsize=24)
plt.ylabel(r"Fraction of particles ",fontsize=24)
if options.save_class_dis_particles:
	plt.savefig(options.save_class_dis_particles,dpi=90)
if options.show_fig:
	plt.show()

# plot class distribution of iteration
plt.clf()
plt.plot(np.arange(1,nr_iters + 1),RandomRef_inEachIteration)
plt.xlabel(r"Iterations",fontsize=24)
plt.ylabel(r"Fraction of phase-randomized class",fontsize=24)
if options.save_class_dis_iteration:
	plt.savefig(options.save_class_dis_iteration,dpi=90)
if options.show_fig:
	plt.show()

if options.outputstar:
	# Select particles according to their class distributions
	ptcls_goodClassDist = ptcls_numberInRandomRef <= options.threshold
	f_out=open(options.outputstar,"w")
	laststar=all_stars[-1]
	f=open(laststar,"r")
	j=0
	for line in f:
		ln_s = line.split()
		if (len(ln_s) < 3) :
			f_out.write(line)
		else:
			if ptcls_goodClassDist[j] :
				f_out.write(line)
			j += 1
	f.close()
	f_out.close()
