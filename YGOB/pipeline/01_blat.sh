#!/usr/bin/bash -l
#SBATCH -p short -c 24 --mem 64gb --out logs/blat.%a.log

module load kent-tools
N=${SLURM_ARRAY_TASK_ID}
if [ -z $N ]; then
	N=$1
	if [ -z $N ]; then
		echo "need a slurm job or cmdline option"
		exit
	fi
fi
IN=$(ls query/*.pep | sed -n ${N}p)
NAME=$(basename $IN .pep)
DB=AA.fsa
OUTDIR=results
EXT=blat.tab
mkdir -p $OUTDIR
echo $OUTDIR/$NAME.$EXT
blat -out=blast8 -prot $DB $IN $OUTDIR/$NAME.$EXT
