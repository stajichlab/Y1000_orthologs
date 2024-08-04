#!/usr/bin/bash -l
#SBATCH -N 1 -c 16 --mem 24gb --out logs/orthofinder.%A_%a.log -p short

mkdir -p logs
module load orthofinder
opt="" # could change to "-C xeon" and will run on the xeon nodes; # could change this to empty and will run on any node
JOBS=orthofinder_steps.diamond.sh
LOG=orthofinder_steps.diamond.log
CHUNK=1000
TMPJOBS=tmpjobs
mkdir -p $TMPJOBS
export TEMPDIR=$SCRATCH
if [ ! -f $LOG ]; then
	orthofinder -op -t 16 -a 16 -f input -S diamond_ultra_sens -o OrthoFinder_diamond > $LOG
fi
if [ ! -f $JOBS ]; then
	grep ^diamond $LOG | grep -v 'commands that must be run' | perl -p -e 's/-p 1/-p 8/g;'> $JOBS
fi
# s/^(.+ -o )(\S+)(.+)/if \[ ! -f $2.gz ]\; then $1$2$3; fi/'
t=$(wc -l $JOBS | awk '{print $1}')
MAX=$(expr $t / $CHUNK)
WINDOWSIZE=10
N=1

if [ ! -z "$SLURM_ARRAY_TASK_ID" ]; then
	N=$SLURM_ARRAY_TASK_ID
elif [ ! -z "$1" ]; then
	N=$1
fi
WINDOWSTART=$(perl -e "printf('%d',1 + $WINDOWSIZE * ($N - 1))")
WINDOWEND=$(perl -e "printf('%d',$WINDOWSIZE * $N)")

if [ $WINDOWEND -gt $MAX ]; then
	echo "N ($N) for slurmjob is too big";
	$WINDOWEND=$MAX
fi
echo "t is $t MAX is $MAX WINDOWSTART is $WINDOWSTART WINDOWEND is $WINDOWEND"
for n in $(seq $WINDOWSTART $WINDOWEND)
do
	START=$(perl -e "printf('%d',1 + $CHUNK * ($n - 1))")
	END=$(perl -e "printf('%d',$CHUNK* $n)")
	if [ ! -f $TMPJOBS/job_${n}.sh ]; then
	    echo "#!/usr/bin/bash -l" > $TMPJOBS/job_${n}.sh
	    echo "module load diamond" >> $TMPJOBS/job_${n}.sh
	    sed -n ${START},${END}p $JOBS | while read LINE 
	    do
		f=$(echo $LINE | perl -p -e 's/.+-o (\S+).+/$1/')
		if [ ! -e $f.gz ]; then
		    echo $LINE
		fi
	    done >> $TMPJOBS/job_${n}.sh 
	    count=$(wc -l $TMPJOBS/job_${n}.sh | awk '{print $1}')
	    if [ $count -gt 2 ]; then	
		sbatch -p epyc $out --out logs/diamond.$n.log -J Dmd$n -N 1 -n 1 -c 8 --mem 4gb $TMPJOBS/job_${n}.sh
	    else
		echo "skipping $n no jobs to run"
		# rm $TMPJOBS/job_${n}.sh
	    fi
	fi
done
