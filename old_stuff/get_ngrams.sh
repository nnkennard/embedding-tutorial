#!/bin/bash
#SBATCH --job-name=ngramArray
#SBATCH --nodes=1 --ntasks=1
#SBATCH --output=logs/test_%A_%a.out
#SBATCH --error=logs/test_%A_%a.err
#SBATCH --array=0-36

array=( $(seq 0 9 ) )
for c in {a..z}
do
	array[${#array[@]}]=$c
done
array[${#array[@]}]="_"

python get_ngrams_quickly.py -p ${array[$SLURM_ARRAY_TASK_ID]}
