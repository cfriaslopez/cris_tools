import pathlib
import sys
import os


#import pdb; pdb.set_trace()
################################
# declare vars , not say declare, assign value 
# Units
kilo = int(10**3)
giga = int(10**9)

###############################
# search file with old "label"
file_old_cluster = glob.glob("*old*")
print(file_old_cluster) # return a list ['sizes_old_cluster_test.tab']

len_files=len(file_old_cluster)

print(len_files)#1

## chequear que solo hay un file
if len(file_old_cluster) != 1:
    print("more than one file")
    sys.exit(1) # because 0 means terminate the program without problems

# initializing_delim
#delim = "_"

old_dict = dict()

# open file with old label
with open(file_old_cluster[0], 'r') as file_old:
    #line_strip = file_old.readlines().strip() # can not do strip because return a list 
    #line_strip = file_old.readline().strip()# works but just one line is reported
    #print(line_strip)
    #lines = file_old.readlines()# printa todo como si fuera una lista
    #print(lines)
    for line in file_old:
        print(line) # 20K       /scratch/project/production/shared/minionRAWDATA/20141105_LYNX_749K_48H_cnaglab1_MN2065784_20150122_r7.x_2D_basecalling_rev1.9.tar
        line_p = line.strip () #remove newline character at end of each line
        size, filepath = line_p.split('\t') # split by tab
        print(size)
        #print(filepath)
        file_name_old=os.path.basename(filepath)
        #print(file_name_old)
        old_dict[file_name_old] = size
        # check if last element size is 
        #if str1.startswith('"') and str1.endswith('"'):#
        num = float(size[:-1])#20
        unit = size[-1]#K
        #if size[:-1].endswith('K'):
        if unit == 'K':
            #num_no_units = num * f"{kilo}" # 10001000100010001000100010001000100010001000100010001000100010001000100010001000
            num_no_units = num * kilo
            print("num_no_units %s" %(num_no_units))
        #elif size[:-1].endswith('G'):
        elif unit == 'G':
            num_no_units = num * giga
            print("new size %s" %(num_no_units))
        else:
            #print("Unit %s not found in db"%(size[:1]))
            print("Unit %s not found in db"%(unit))
            sys.exit(1)

                #://realpython.com/python-f-strings/#the-modulo-operator        #                        
#print("size %s and file %s" %(size,file_name_old))

print(file_name_old, old_dict[file_name_old])
# printing result
print("old cluster : "+ str(old_dict))
#old cluster : {'20141105_LYNX_749K_48H_cnaglab1_MN2065784_20150122_r7.x_2D_basecalling_rev1.9.tar': '20K', '20141105_LYNX_749K_cnaglab2_48H_MN2065520_20150121_r7.X_2D_basecalling_rev1.9': '4.0K', '20160202_OSSOWSKI01_AA9708_319T_cnaglab1_48h_FAA86274': '8.0K', '20160209_OSSOWSKI01_AA9708_385T_canglab2_48H_FAA87350': '4.0K', '20161103_COLIBRI_01_306Y_CRGpc2_48H_FAB43121': '400G', '20161214_SpiderMite_LE_crgPC1_48H_FAB42904_R9': '34G', '20161214_SpiderMite_LES_CRGpc2_48H_FAB42879_R9': '104G'}

#for key in old_dict:
#    value = old_dict[key]
#    print(key, value)

# there are two columns
#20K    /scratch/project/production/shared/minionRAWDATA/20141105_LYNX_749K_48H_cnaglab1_MN2065784_20150122_r7.x_2D_basecalling_rev1.9.tar
#4.0K   /scratch/project/production/shared/minionRAWDATA/20141105_LYNX_749K_cnaglab2_48H_MN2065520_20150121_r7.X_2D_basecalling_rev1.9
# extract the name of the file 
# store the content in a dictionary
# key = name file
# value = size of the file, first column
