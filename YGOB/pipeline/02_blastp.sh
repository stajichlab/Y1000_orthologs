#!/usr/bin/bash -l
#SBATCH -p short -c 24 --mem 64gb --out logs/blastp.%a.log

module load ncbi-blast
N=${SLURM_ARRAY_TASK_ID}
if [ -z $N ]; then
	N=$1
	if [ -z $N ]; then
		echo "need a slurm task job or cmdline option"
		exit
	fi
fi
IN=$(ls query/*.pep | sed -n ${N}p)
NAME=$(basename $IN .pep)
DB=AA.fsa
OUTDIR=results
EXT=BLASTP.tab
mkdir -p $OUTDIR

blastp -query $IN -db $DB -subject_besthit -num_threads 24 \
	-outfmt 6 -out $OUTDIR/$NAME.$EXT -task blastp-fast -use_sw_tback -max_target_seqs 5

