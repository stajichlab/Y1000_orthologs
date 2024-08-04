#!/usr/bin/bash
#SBATCH -p short -N 1 -n 1 --mem 1gb --out logs/mmseqs_batch.%a.log 

FILE=$(realpath commands.sh)
N=${SLURM_ARRAY_TASK_ID}

if [ -z $N ]; then
    N=$1
    if [ -z $N ]; then
        echo "Need an array id or cmdline val for the job"
        exit
    fi
fi
cmd=$(sed -n ${N}p $FILE)
pushd orthofinder
IFS=";"
for line in $cmd
do
	$(module load orthofinder; $line)
done
