#!/bin/tcsh
#$ -pe XXXqueueXXX XXXnodesXXX
#$ -l dedicated=XXXdedicatedXXX 
#$ -e XXXerrfileXXX
#$ -o XXXoutfileXXX
#$ -A Relion 
#$ -cwd
#$ -S /bin/tcsh

# Environment
source ~/.cshrc

mpiexec -n XXXmpinodesXXX  XXXcommandXXX
