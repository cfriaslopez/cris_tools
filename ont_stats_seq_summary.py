import glob
import pandas as pd


targetDir="/home/groups/pbt/cfrias/cris_tools/scripts_cfrias/ont/add_stats_from_seq_summary/20250324_TEST_218_9305AJ_BB6562_X5_1_PBC70961_Test"


summaryFiles = glob.glob("%s/sequencing_summary.*.txt"%targetDir)
#summaryFiles = glob.glob("%s/sequencing_summary.0._100_*.txt"%targetDir)
#summaryFiles
#['/home/groups/pbt/cfrias/cris_tools/scripts_cfrias/ont/add_stats_from_seq_summary/20250324_TEST_218_9305AJ_BB6562_X5_1_PBC70961_Test/sequencing_summary.0.txt']

## create dict
stats_dict_total = {'mean_qscore_template' : [] , 'sequence_length_template' : [] , 'read_id': []}
stats_dict_pass = {'mean_qscore_template' : [] , 'sequence_length_template' : [] , 'read_id': []}
stats_dict_fail = {'mean_qscore_template' : [] , 'sequence_length_template' : [] , 'read_id': []}



## loop for process all the seq_summaty
for isummaryFile in summaryFiles  :
    ibarcode = isummaryFile.split('.')[-2]

    ## open file
    f = open(isummaryFile,'r')

    ## extract columns of interest
    fields =  f.readline()
    num_col_mean_qscore_template = fields.split().index( 'mean_qscore_template' )
    num_col_sequence_length_template = fields.split().index( 'sequence_length_template' )
    num_col_read_id = fields.split().index( 'read_id' )

    ## create dict
    #stats_dict_total = {'mean_qscore_template' : [] , 'sequence_length_template' : [] , 'read_id': []}
    #stats_dict_pass = {'mean_qscore_template' : [] , 'sequence_length_template' : [] , 'read_id': []}
    #stats_dict_fail = {'mean_qscore_template' : [] , 'sequence_length_template' : [] , 'read_id': []}

    ## create dictionaries
    #stats_dict_total = {'mean_qscore_template' : [] , 'sequence_length_template' : [] , 'read_id': []}
    #stats_dict_pass = {'mean_qscore_template_pass' : [] , 'sequence_length_template_pass' : [] , 'read_id_pass': []}
    #stats_dict_fail = {'mean_qscore_template_fail' : [] , 'sequence_length_template_fail' : [] , 'read_id_fail': []}

    ## go to lines file
    for iline in f :
       stats_dict_total['mean_qscore_template'].append( float(iline.split('\t')[num_col_mean_qscore_template] ))
       stats_dict_total['sequence_length_template'].append( int(iline.split('\t')[num_col_sequence_length_template]) )
       stats_dict_total['read_id'].append( iline.split('\t')[num_col_read_id] )

       value_mean_qscore_template = float(iline.split('\t')[num_col_mean_qscore_template])

       ### Pass stats
       #print(value_mean_qscore_template)

       ## si le pongo '10' me dice que es un str
       if ( value_mean_qscore_template >= 10) :
         stats_dict_pass['mean_qscore_template'].append( float(iline.split('\t')[num_col_mean_qscore_template] ))
         stats_dict_pass['sequence_length_template'].append( int(iline.split('\t')[num_col_sequence_length_template]) )
         stats_dict_pass['read_id'].append( iline.split('\t')[num_col_read_id] )

       ### Fail stats
       elif (value_mean_qscore_template <= 10) :
          stats_dict_fail['mean_qscore_template'].append( float(iline.split('\t')[num_col_mean_qscore_template] ))
          stats_dict_fail['sequence_length_template'].append( int(iline.split('\t')[num_col_sequence_length_template]) )
          stats_dict_fail['read_id'].append( iline.split('\t')[num_col_read_id] )

    f.close()

    #import pdb; pdb.set_trace() 
    ### Data frame total stats
    tot_nreads2 = 0
    df_total = pd.DataFrame(stats_dict_total)
    df_total = df_total.sort_values(by='sequence_length_template')
    yyield_total = df_total['sequence_length_template'].sum()
    nreads_total = len( df_total )
    tot_nreads2 += nreads_total
    cumsum = 0
    for i in df_total['sequence_length_template'] :
       cumsum += i
       if ( cumsum > yyield_total/2.0) : break
    N50_total = i
    #
    #medians_total = df_total.median()
    medians_total = df_total.median(numeric_only='True')
    means_total = df_total.mean(numeric_only='True')
    maxs_total = df_total.max(numeric_only='True')
    ncounts_total = str( int(round( nreads_total /1000.0)))
    yieldpfStr_total = str( int(round(yyield_total/1.0e6) ))

    ### Data frame total stats
    tot_nreads2_pass = 0
    df_pass = pd.DataFrame(stats_dict_pass)
    df_pass = df_pass.sort_values(by='sequence_length_template')
    yyield_pass = df_pass['sequence_length_template'].sum()
    nreads_pass = len( df_pass )
    tot_nreads2_pass += nreads_pass
    cumsum = 0
    for j in df_pass['sequence_length_template'] :
        cumsum += j
        if ( cumsum > yyield_pass/2.0) : break
    #N50_pass = N50_total -i 
    N50_pass = j
    medians_pass = df_pass.median(numeric_only='True')
    means_pass = df_pass.mean(numeric_only='True')
    maxs_pass = df_pass.max(numeric_only='True')
    ncounts_pass = str( int(round( nreads_pass /1000.0) ) )
    #pct_total_reads =nreads_pass * 100.0/tot_nreads2
    yieldpfStr_pass = str( int(round(yyield_pass/1.0e6) ))

    #pct of passs reads
    pct_total_reads =nreads_pass * 100.0/tot_nreads2

    n_50_value = N50_pass

    lw_payload = { "total_reads": ncounts_total, "total_yield": yieldpfStr_total, 'clusters_pass_filt' : ncounts_pass, "yield_pass_filt": yieldpfStr_pass, "percent_total_reads": pct_total_reads, 'status' : '/lims/api/seq/loadedwithstatus/5', 'n50': n_50_value}
    print(lw_payload)
