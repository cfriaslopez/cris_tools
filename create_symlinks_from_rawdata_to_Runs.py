import datetime
from datetime import datetime
from datetime import timedelta
import glob
import os
import pandas as pd
import re
import pathlib
from pathlib import Path

"""
script for 1) create links in Runs of pod5 and 2) manually remove the merged pod5 after check the size
"""


## VAR
PATH_RAW_DATA='/scratch_isilon/groups/pbt/data/project/production/promethion01/raw_data'
PATH_RUNS='/scratch_isilon/groups/pbt/data/project/production/promethion01/'

## LIST FILE
#RAW_DATA_FILE='directories_with_pod5_noempty.tab'
RAW_DATA_FILE='directories_with_pod5_noempty_dirname_unique.tab'
#./240513_PILC_07_8924AI_PAW45962/240513_PILC_07_8924AI_PAW45962/240513_PILC_07_8924AI_PAW45962/20240513_1649_1F_PAW45962_90cbf86f/pod5
#./240416_TEST/240416_TEST/240416_TEST/20240416_1515_1D_PAW05229_6d401c23/pod5
#mv directories_with_pod5_noempty.tab directories_with_pod5_noempty.tab_bkp
# remove .
#sed -e 's/.//' directories_with_pod5_noempty.tab_bkp >> directories_with_pod5_noempty.tab
#/240513_PILC_07_8924AI_PAW45962/240513_PILC_07_8924AI_PAW45962/240513_PILC_07_8924AI_PAW45962/20240513_1649_1F_PAW45962_90cbf86f/pod5
#/240416_TEST/240416_TEST/240416_TEST/20240416_1515_1D_PAW05229_6d401c23/pod5

## PATH + FILES
PATH_RAW_DATA_FILE = os.path.join(PATH_RAW_DATA, RAW_DATA_FILE)


############################## #############################  open main
def main():
    ############################# open DIR_RAW_DATA_FILE and iterate every line
    ## save the path to create the link
    ## examples
    #/240422RIMI_IAMAN_59_8067AI_PAW99963/240422_IRIMIAMAN_59_8067AI_PAW99963/240422_IRIMIAMAN_59_8067AI_PAW99963/20240422_1628_1G_PAU99963_1d8cfa9a/pod5
    #/240108_OMICSRDLR_02_4392AI_PAQ36329/240108_OMICSRDLR_02_4392AI_PAQ36329/240108_OMICSRDLR_02_4392AI_PAQ36329/20240108_1521_1F_PAQ36329_c9f95847/pod5_pass
    #/240108_OMICSRDLR_02_4392AI_PAQ36329/240108_OMICSRDLR_02_4392AI_PAQ36329/240108_OMICSRDLR_02_4392AI_PAQ36329/20240108_1521_1F_PAQ36329_c9f95847/pod5_fail
    #/240118_OMICSRDLR_02_4945AI_PAS00419-run2/240118_OMICSRDLR_02_4945AI_PAS00419-run2/240118_OMICSRDLR_02_4945AI_PAS00419-run2/20240118_1048_2F_PAS00419_8d58630a/pod5_pass
    #/240118_OMICSRDLR_02_4945AI_PAS00419-run2/240118_OMICSRDLR_02_4945AI_PAS00419-run2/240118_OMICSRDLR_02_4945AI_PAS00419-run2/20240118_1048_2F_PAS00419_8d58630a/pod5_fail
    #/240702_BGE_123_0996AJ_PAW46755/240702_BGE_123_0996AJ_PAW46755/240702_BGE_123_0996AJ_PAW46755/20240702_1149_2H_PAW46755_5119f5c3/pod5_skip


    ## open file and store in array
    file = open(PATH_RAW_DATA_FILE)
    content = file.readlines()

    ## pattern to search if there are two runs
    pattern_run2 = r"run2$"
    
    num = 0
    ## loop to iterate over line's array
    for line in content:
        #dir_line = re.sub(r"\n", "",content[0])

        dir_line = re.sub(r"\n", "",line)
        # check the dir; create the dir
        #num_files_glob = glob.glob('./[0-9].*'))
        #num_files_glob = glob.glob('./[0-9].*'))
        pod5_files = glob.glob(PATH_RAW_DATA + dir_line + "/**/*.pod5", recursive=True)
        len_pod5_files = len(pod5_files)

        final_sum_file_list = glob.glob(PATH_RAW_DATA + dir_line + "/**/final_summary*", recursive=True)
        # /scratch_isilon/groups/pbt/data/project/production/promethion01/raw_data/240902_CBP_68_1878AJ_PAW80524/240902_CBP_68_1878AJ_PAW80524/240902_CBP_68_1878AJ_PAW80524/20240902_1615_2B_PAW80524_6ef0b7df
        # pod5_files_in_final_dest=123
        # pod5_files_in_fallback=0
        print (dir_line)
        with open (final_sum_file_list[0], 'r') as final_sum_file:
            content_final_sum_file = final_sum_file.read().replace('\n', ',')
        ## pass to a list
        content_final_sum_file_list = content_final_sum_file.split(",")
        b = 'pod5'
        ## 
        res = list(filter(lambda x: b in x, content_final_sum_file_list))
        # me quedo aqui que tengo que sumar los pod5
        pod5_info_content_final_sum_file_list = res[0].split("=")
        num_files_pod5_from_final_sum = pod5_info_content_final_sum_file_list[1]
            # count the number of pod5 files
        #sbsuser@login6:/scratch_isilon/groups/pbt/data/project/production/promethion01/raw_data/231218_BGE_39_3996AI_PAQ36392-run2/231218_BGE_39_3996AI_PAQ36392-run2/231218_BGE_39_3996AI_PAQ36392-run2/20231218_1718_2G_PAQ36392_6e51a90e$ find . -name *pod5 -type f | wc -l
        #1325
        # check the number of pod5 in sequencing_summary_PAW80524_6ef0b7df_0ed5e444.txt
        if (int(num_files_pod5_from_final_sum) == len_pod5_files):
            create_link = "yes"
        else:
            create_link = "no"
        ## if create_link equal to yes
        if (create_link == "yes"):
            print(dir_line + " " + "correct_pod5_file_number")
        else:
            print(dir_line + " " + "wrong_pod5_file_number")
        

    # me quedo aqui 251211 
if __name__ == "__main__":
    main()


    path_dir_split = dir_line.split("/")
    name_dir = path_dir_split[1]
    # split dir by _  "240702_BGE_123_0996AJ_PAW46755"
    name_dir_string = name_dir.split("_")
    # get the last element of array -
    last_name_dir_string = (name_dir_string [-1])
    pattern_to_find = " "
    # check if there two runs
    if re.match(last_name_dir_string, pattern_run2):
        split_FC_ID = last_name_dir_string ("-")
        FC_Name = split_FC_ID[0]
        run = 2
        FC_to_find = "*" + "2_" + FC_Name
        pattern_to_find = FC_to_find
        else:
        FC_ID = last_name_dir_string
        FC_to_find = FC_ID
        pattern_to_find = "*" + FC_to_find

    ## check if the pattern exist in Runs
    dir_exist = glob.glob(os.path.join(PATH_RUNS, pattern_to_find)) 

    # check if dir_exist is TRUE
    if dir_exist:
        print(dir_exist"+""dir_exist in Runs")
        ## create the symbolic lunk of the path stored 
    else:
        print(last_name_dir_string "+" "dir_exist in Runs")

############################# #############################close main
if __name__ == "__main__":
    main()
