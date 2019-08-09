#!/bin/bash 
#
#SBATCH -J CPL-2
#SBATCH -N 7
#SBATCH -n 126
#SBATCH -t 3-00:00:00
#SBATCH --ntasks-per-node=18
#SBATCH --ntasks-per-core=1 
#SBATCH -o job.out # STDOUT 
#SBATCH -e job.err # STDERR 

rm ../../../CASE-2_CPL/GRAPHIQUES/graph*.nc tmp/* fort.* debug* SYMP*.nc WW3*.nc; mpirun -np 80 ./S26.exe : -np 46 ./ww3_shel
