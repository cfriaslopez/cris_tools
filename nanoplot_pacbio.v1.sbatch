#!/bin/bash
#SBATCH -J Nanoplot_PacBIO
#SBATCH -q normal
#SBATCH --mem 300G
#SBATCH -c 100 # cpu per task
#SBATCH -t 12:00:00 # TimeLimit (D-HH:MM)
#SBATCH -o slurm.%N.%j.out # STDOUT
#SBATCH -e slurm.%N.%j.err # STDERR
#SBATCH --mail-type=END,FAIL # notifications for job done & fail
##SBATCH --mail-user=cristina.frias@cnag.eu # send-to address


module use /software/pbt/modules/all
module load SAMtools
module load NanoPlot

DIR=$(pwd)

#mkdir -p /scratch_isilon/groups/pbt/data/project/lims/revio/$FC_name/1/
#cp *html /scratch_isilon/groups/pbt/data/project/lims/minion_qc/$FC_name/1/
#/scratch_isilon/groups/pbt/data/project/production/promethion02/Runs_stopped/run_stopped_260126_LUCIA_54_P9371_PBK41264/mapping_qc/reads_input/nanoplot_individual_fastq

# lane o run
run=1

############ hifi reads
#movie_id_file_name=m84289_260316_132024_s4.hifi_reads.bc2087.bam
for filename in $(ls *'hifi_reads'*.bam)
do
   movie_id_name=$(echo $filename | cut -f 1 -d '.')
   index=$(echo $filename | cut -f 3 -d '.')
   NanoPlot -t 100 --ubam $filename --prefix $movie_id_name"_"$index"_"$run"_" -o $index"_pass_reads"
   mkdir -p /scratch_isilon/groups/pbt/data/project/lims/revio/$movie_id_name/1/$index
   cp  $index"_pass_reads"/* $index /scratch_isilon/groups/pbt/data/project/lims/revio/$movie_id_name/1/
done

#NanoPlot -t 100 --ubam $filename --tsv_stats --prefix $movie_id_name"_"$index"_"$run"_" -o $index

############ fail reads
for filename in $(ls *'fail_reads'*.bam)
do
   movie_id_name=$(echo $filename | cut -f 1 -d '.')
   index=$(echo $filename | cut -f 3 -d '.')
   NanoPlot -t 100 --ubam $filename --prefix $movie_id_name"_"$index"_"$run"_fail" -o $index"_fail_reads"
   
done

"""
NO filter these reads and don't use
############ unassigned reads
for filename in $(ls *'fail_reads'*.bam)
do
   movie_id_name=$(echo $filename | cut -f 1 -d '.')
   index=$(echo $filename | cut -f 3 -d '.')
   NanoPlot -t 100 --ubam $filename --prefix $movie_id_name"_"$index"_"$run"_fail" -o $index"_fail_reads"
   
done
"""
