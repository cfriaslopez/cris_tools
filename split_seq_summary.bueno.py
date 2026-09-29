import pandas as pd

## pass as argument 1
#https://stackoverflow.com/questions/20157824/how-to-take-input-file-from-terminal-for-python-script
import sys
#import pdb; pdb.set_trace()
#inFile = sys.argv[1]
#outFile = sys.argv[2]

inFile_1 = sys.argv[1]
inFile_2 = sys.argv[2]
outFile = sys.argv[3]

#with open(inFile,'r') as i:
    #lines = i.readlines()

#processedLines = manipulateData(lines)

#with open(outFile,'w') as o:
    #for line in processedLines:
        #o.write(line)


# pass argument like a list
#read_id_data = [line.strip() for line in open("/home/cfrias/cnag/ONT/2024/CERVERAJOS_03/240515_CERVERAJOS_03_9023AI_FAY22383-Rebasecalling_without_qscore_filter_FASTQ/create_seq_summary_withFASTQ/test_FAY22383_dorado-basecaller_0.7.0_sup.No_qscore_filter.fastq_read_id.tab", 'r')]

#import pdb; pdb.set_trace()
read_id_data = [line.strip() for line in open(inFile_1, 'r')]
read_id_data.sort(reverse=False)

## pass as argument 2
#sequencing_summary_csv = pd.read_csv("/home/cfrias/cnag/ONT/2024/CERVERAJOS_03/240515_CERVERAJOS_03_9023AI_FAY22383-Rebasecalling_without_qscore_filter_FASTQ/create_seq_summary_withFASTQ/test_sequencing_summary_FAY22383_d7e66c02_2d4de5b5.txt", sep='\t')

sequencing_summary_csv = pd.read_csv(inFile_2, sep='\t')

# Sorting by column 'Country'
#df.sort_values(by=['Country'])
#sequencing_summary_csv.sort_values(by=['read_id'])
seq_summary_sort_asc = sequencing_summary_csv.sort_values(by=['read_id'], ascending=True)

sequencing_summary_csv_header = list(sequencing_summary_csv)
#print(sequencing_summary_csv_header)
#['filename_fastq', 'filename_fast5', 'filename_pod5', 'parent_read_id', 'read_id', 'run_id', 'channel', 'mux', 'minknow_events', 'start_time', 'duration', 'passes_filtering', 'template_start', 'num_events_template', 'template_duration', 'sequence_length_template', 'mean_qscore_template', 'strand_score_template', 'median_template', 'mad_template', 'pore_type', 'experiment_id', 'sample_id', 'end_reason']
#read_id_csv_length = len(read_id_csv)
#print(read_id_csv_length)
#9515714
#output_file = 'sequencing_summary_FAY22383_rebasecalling_dorado_0.7.0.txt'
output_file = outFile

# Creating Empty DataFrame and Storing it in variable df
df_result = pd.DataFrame(columns=sequencing_summary_csv_header)

# iterate over the dataframe
#for ind in df.index:
    #print(df['Name'][ind], df['Stream'][ind])
    #sequencing_summary_csv_selected_rows =  sequencing_summary_csv[(sequencing_summary_csv.read_id == x)]
    #sequencing_summary_csv_selected_rows =  sequencing_summary_csv[(sequencing_summary_csv.read_id == "@d9031165-09ab-4395-807b-db9d04ab5fb1" )] # no lleva @
    #sequencing_summary_csv_selected_rows =  sequencing_summary_csv[(sequencing_summary_csv.read_id == "9f99fab2-a76a-43fa-8b4e-11bdad1d31d1")]

# iterate over the list
#https://www.w3schools.com/python/python_lists_loop.asp
#for i in range(len(read_id_data)):
    #print(read_id_data[i])
    #sequencing_summary_csv_selected_rows =  sequencing_summary_csv[(sequencing_summary_csv.read_id == read_id_data[i])]
    #print(sequencing_summary_csv_selected_rows)
    # append the new row to the DataFrame
    #df_result = df_result.append(sequencing_summary_csv_selected_rows, ignore_index=True)
    #df_result.loc[len(df_result)] = sequencing_summary_csv_selected_rows
    # https://www.geeksforgeeks.org/how-to-add-one-row-in-an-existing-pandas-dataframe/
    #df = df._append(df2, ignore_index = True)
    # funciona en mi pc, pero no en cluster
    #df_result = df_result._append(sequencing_summary_csv_selected_rows, ignore_index=True)
    #print(df[df['age'] < 25])
    #print(sequencing_summary_csv[sequencing_summary_csv['read_id'] == read_id_data[i]])
    #sequencing_summary_csv_selected_rows = sequencing_summary_csv[sequencing_summary_csv['read_id'] == read_id_data[i]]
    #sequencing_summary_csv_selected_rows = seq_summary_sort_asc[seq_summary_sort_asc['read_id'] == read_id_data[i]]    
    #print(sequencing_summary_csv_selected_rows)
    #pd.concat([df2, df])
    #pd.concat([sequencing_summary_csv_selected_rows, df_result])
    #https://stackoverflow.com/questions/24284342/insert-a-row-to-pandas-dataframe
    #df_result = pd.concat([sequencing_summary_csv_selected_rows, df_result], ignore_index=False)
    #print(df_result)
    #df_result = sequencing_summary_csv[sequencing_summary_csv['read_id'].str.contains(read_id_data[i])]
    #print(df_result)
    #https://www.tutorialspoint.com/how-to-write-pandas-dataframe-as-tsv-using-python
    #df_result.loc[len(df_result)] = sequencing_summary_csv_selected_rows
    #my_list = [1, 2, 3]
results = sequencing_summary_csv.loc[sequencing_summary_csv["read_id"].isin(read_id_data)]
print(results)

#df_result.to_csv(output_file, sep='\t', index=False, header=True)
results.to_csv(output_file, sep='\t', index=False, header=True)



# importing pandas as pd 
#import pandas as pd 

# reading csv file 
#df = pd.read_csv("Assignment.csv") 

# filtering the rows where Credit-Rating is Fair 
#df = df[df['Credit-Rating'].str.contains('Fair')] 
#print(df) 



""""" comments
##############################################
#>>> df_result = pd.DataFrame()
#>>> print(df_result)
#Empty DataFrame
#Columns: []
#Index



#df4= pd.DataFrame(index = range(5), columns=["col1", "col2", "col3", "col4"])
#df4= pd.DataFrame(columns=sequencing_summary_csv_header)
"""""
