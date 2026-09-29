#!/bin/bash
#SBATCH --job-name=rsync_BCLLATLAS_240
#SBATCH --output=rsync_BCLLATLAS_240_%A_%a.out
#SBATCH --error=rsync_BCLLATLAS_240_%A_%a.err
## edit below the number of jobs
#SBATCH --array=0-4
#SBATCH --cpus-per-task=4
#SBATCH --time=12:00:00
#SBATCH --qos=normal
######SBATCH --partition=genD
#####SBATCH --partition=scratch
#SBATCH --partition=production
#SBATCH --account=sa_pbt


module use /software/modules/all
#module load GCC/14.3.0
#module load BLAST+/2.17.0-gompi-2025b
#module load SAMtools/1.22.1-GCC-14.3.0

LINE=$((SLURM_ARRAY_TASK_ID+1))
FILE=$(sed "${LINE}q;d" *.list)

set -e

# to rsync every path in the list file 
#rsync -azvPL $FILE /scratch_isilon/groups/statgen/eraineri/ 
rsync -azvPL $FILE  /shared/pbt/transfers/

"""
# Need a Input file with the dir_fc.list
/scratch_isilon/groups/pbt/cfrias/ont02/output/240227_BCLLATLAS_240_6132AI_PAU78289_rebasecalling
/scratch_isilon/groups/pbt/cfrias/ont03/output/240130_BCLLATLAS_240_5299AI_PAU39444-Rebasecalling
"""

