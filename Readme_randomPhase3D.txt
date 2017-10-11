
Run RELION with random_phase 3D classification option:
	Add following line to "Additional arguments" of 3D classification section in GUI of RELION, and substitute "low_res" and "high_res" with desired value. Options "--random_phase_res" and "--random_phase_res_upper_limit" determine the lower and upper resolution limit for phase-randomizing, respectively.
		--random_phase_otherrefs --random_phase_res "low_res" --random_phase_res_upper_limit "high_res"	
	The default value for "--random_phase_res_upper_limit" is 1 Angstrom. It is better to use this default value than some other values according to our experience. So, you can just input the first two options:
		--random_phase_otherrefs --random_phase_res "low_res"
	You can also attach the above option line to the RELION command line generated with "Print command" button in RELION GUI.
	After doing as above, run RELION 3D classification as routine procedure. The iteration number can be set to a larger value than the default value "25".
	

Analyze results and remove bad particles:
	# Modify following file and then run it:
	plot_randomPhase3D.sh
	This shell script runs a python script "plotStatofRandomPhaseRef.py".
