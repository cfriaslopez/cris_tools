#!/usr/bin/env bash

## add FC to rebasecall

dorado=/home/groups/pbt/cfrias/software_gpu01h200/dorado-1.0.2-linux-x64

work_dir=/scratch_isilon/groups/pbt/cfrias/gpu01h200/output_rebasecalling
#input=/scratch_isilon/groups/pbt/data/project/production/gridion01/raw_data
input=/production/promethion03/Runs
#model=sup,5mC_5hmC,6mA
model=sup,5mC_5hmC
dorado_version=dorado-1.0.2-linux-x64
#molecule=rna#dna or rna
molecule=dna

#### model name
model_name=$(sed 's/,/-/g' <<<"${model}")
# only one model
#model_name=${model}
cuda=$1

### SUP 

function rebasecall {
    fcdir="$1"

    # if the directory doesn't exist
    if [ ! -d "${work_dir}/${fcdir}_${model_name}_${molecule}_${dorado_version}_rebasecalling" ]; then
        mkdir "${work_dir}/${fcdir}_${model_name}_${molecule}_${dorado_version}_rebasecalling"
    fi

    cd "${work_dir}/${fcdir}_${model_name}_${molecule}_${dorado_version}_rebasecalling"

    #call dorado methylation
    ${dorado}/bin/dorado basecaller \
    ${model} \
    ${input}/${fcdir}/ -vv -r -x "cuda:${cuda}" \
    > ${fcdir}_${dorado_version}_${model_name}_${molecule}.No_qscore_filter.bam \
    2> ${fcdir}_${dorado_version}_${model_name}_${molecule}.No_qscore_filter.bam.log

    #create summary
    ${dorado}/bin/dorado summary ${fcdir}_${dorado_version}_${model_name}_${molecule}.No_qscore_filter.bam > ${fcdir}_${dorado_version}_${model_name}_${molecule}.No_qscore_filter.bam.tsv

}

#launch the rebasecalls

#rebasecall "FAX15993" # ont01
#rebasecall "241111_GOMEZPIL_03_3854AJ_PB24540"
rebasecall "$2"
#rebasecall "$3"
#rebasecall "$4"
