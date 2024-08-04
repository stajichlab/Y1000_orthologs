#!/usr/bin/bash -l
#SBATCH --out download.log -c 4 -N 1 -n 1
# download
curl -L -o y1000p_pep_files.tar.gz https://plus.figshare.com/ndownloader/files/40534997
# uncompress
pigz -dc y1000p_pep_files.tar.gz | tar xf -

