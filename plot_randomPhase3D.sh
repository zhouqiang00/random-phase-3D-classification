#!/bin/bash
# Written by Zhou Qiang @ Yan lab, School of Medicine, Tsinghua University.
for i in Class3D/*_it001_data.star
# We generally run about 30-50 iterations for a 3D classification cycle.
do
	b=${i/_it001_data.star/}
	echo $b
	/path/to/plotStatofRandomPhaseRef.py -i ${i} -d ${b}.dat --save_class_dis_particles=${b}_lowertimes_cls.png --plot_lower_times 1 --start_iter 5 
	for j in 20 10 0
	# j is the threshold time for bad particles.
	# Use smaller value of j to remove more "bad" particles, but some "good" particles may also be removed.
	#
	do
		/path/to/plotStatofRandomPhaseRef.py -i ${i} -d ${b}.dat --save_class_dis_particles=${b}_ptcls_s5.png --save_class_dis_iteration=${b}_iter_s5.png -o ${b}_startiter5_sel_${j}.star -t ${j} --start_iter 5
	done
done

