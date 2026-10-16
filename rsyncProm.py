#/usr/bin/python3

#program to check flowcells from Promethion and rsync them to scratch

"""This script needs to run every few hours with a Cron job.
    Table must be: name, local size, scratch size, status, time updated.
    Any flowcell to rsync will be set by creating slinks to the directory and rsyncing them.
    Program will exit if /scratch/project/production/promethion01 is not mounted in PromethION.
    Program will exit if another instance of the program is rsyncing files - this can be disabled.

    1.- checks in PromethION directories with "some file" created at the beginning of the flowcell sequencing
    2.- checks table of 'processed flowcells'
    3.- checks all flowcells existing in /scratch/project/production/promethion01
    4.- for each flowcell in PromethION if it was set as "Done" in table, it will ignore it
    5.- either if there is a "final_summary" for that fc in scratch will  check directory size of both promethion and scratch
    6.- if both sizes are the same as in the table and similar between them, will mark fc as "Done" and remove the link
    7.- if fc is new or sizes are different from those saved in table, will save new sizes and add link
    8.- then it will rsync all links to scratch
    9.- then will print the updated table to file
    10.- finally will rsync table to scratch"""

#I run it with 'python3' command
#If in Scratch/ should be RUN WITH PYTHON 3: module load PYTHON/3.8.6
#then: unset PYTHONPATH


## modules
#required module to work with directories
import os
#command line flags library
import argparse
# to get popen outputs
import subprocess
#regex library
import re
#get the time and date library
from datetime import datetime
# to get popen outputs
import subprocess


version = "2.4"
####### Changelog v2.4; 2024-03-27 (MÓskar): 
# fixed rsync for more clear and better use, added some harcoded values to variables
# uncommented some part of the code that were commented out
# fixed an error caused when all links were removed beacuse all had been rsynced, but it tried to rsync anyway
# Other minor edits

####### Changelog v2.3; 2022-04-29 (MÓskar): 
# Set a slightly higher "smalldif" default value (adjusted to real differences found between directory sizes),
# Changed the function that prints the updated table so it sorts the dictionary by date updated
# now "du" command uses flag -b so size should be real bytes and not depending on the file system
# Other minor edits



#global variables
finalfcheck = "final_summary_*.txt" #file that must be present in a flowcell to be recognised as a flowcell
inifcheck = "pore_scan_data_*.csv" #file that must be present in a flowcell to be recognised as a flowcell
processed_fc_filelist = os.path.normpath("/data/fcdir_table.csv") #path to the table of processed flowcells
wpath=os.path.normpath("/data") #working directory
#mountedir = os.path.normpath("/network/mnt") #path to the directory where scratch is mounted
#mountedir = os.path.normpath("/home/prom/mount_isilon/test_login7") #path to the directory where scratch is mounted
#mountedir = os.path.normpath("/home/prom/mount_isilon/I") #path to the directory where scratch is mounted
#mountedir = os.path.normpath("/data/mount_isilon/prom_data")
#mountedir = os.path.normpath("/data/mount_isilon/login7")
mountedir = os.path.normpath("/data/production/promethion01/testing_permissions")
#should_be_there = "X1" #directory that should exist in mounted directory if it has been mounted
should_be_there = "certificate_2024"
warning_msg = "PLEASE_MOUNT_SERVER_TO_PROMETHION"
warning_flag = "ongoing_rsync"
slinks_dir = "/data/auto_rsync_slinks"
homedir="/home/prom"
smalldif=0.016


#define "parser" to hold command line options
parser = argparse.ArgumentParser(description='rsyncPromethion %s will find directories from flowcells, sync them to scratch, and update the table of processed flowcells.\nProgram will fail if server is not mounted.\nTable of processed flowcells must be comma separated with these columns: name, local size, scratch size, status, last updated'%(version) )
parser.add_argument("-w", "--workingdir", required=False, type=str,
    help="path to parent directory with flowcell directories; default: %s"%wpath)
parser.add_argument("-i", "--ini", required=False, type=str,
    help="name pattern for a file that must exist inside flowcell directories to recognise them as flowcells; default: %s"%inifcheck)
parser.add_argument("-e", "--end", required=False, type=str,
    help="name pattern for a file that must exist inside flowcell directories to recognise them as finished; default: %s"%finalfcheck)
parser.add_argument("-t", "--table", required=False, type=str,
    help="name or  path to the processed flocells directory list; default: %s"%processed_fc_filelist)
parser.add_argument("-l", "--links", required=False, type=str,
    help="directory to place the sim links; default: %s"%slinks_dir)
parser.add_argument("-m", "--mounted", required=False, type=str,
    help="path to the directory in which the server is mounted; default: %s"%mountedir)
parser.add_argument("-d", "--difference", required=False, type=float,
    help="difference allowed between flowcell directory sizes: size promethion / size scratch = 1 ± difference; default: %s"%smalldif)
parser.add_argument("-f", "--force", action='store_true',
    help="Add this to force the run even if another instance of rsyncPromethion is already running.")


args = vars(parser.parse_args()) #parses command line arguments to "args" as a variables


### functions
def get_size(path):
    #get actual size of the local directory
    if os.path.isdir(path):
        get_size = "du -sb %s"%(os.path.normpath(path))
        size_dir = os.popen(get_size).read()
        #print (size_dir)
        return int(re.match(r'(^[0-9]*).*', size_dir).group(1))
    else:
        raise Exception("\n\nERROR!\n%s is not a valid directory.\nSize cannot be computed.\n\n"%(path))


def update_flowcell(fc_name, insize, outsize, status):
    """Update dictionary of flowcells,
    deal with links according to status
    and signal that changes have been made
    insize = size of local directory
    outsize = size of directory in scratch
    status = at which stage was the flowcell when processed"""
    
    #update table
    processed_dirs[fc_name]= [insize, outsize, status, now]
    #create/remove links
    one_slink = os.path.join(slinks_dir, fc_name)
    if (status == "Done"):
        if os.path.exists(one_slink):
            os.unlink(one_slink)
    else:
        flowcell_parent = os.path.join(wpath, fc_name)
        if not os.path.exists(one_slink):
            os.symlink(flowcell_parent, one_slink)
        print ("Updated %s links and status."%(fc_name))
    any_change = 1
    return any_change




#get paths
if args["workingdir"]:
    wpath=os.path.normpath(args["workingdir"])

#get paths
if args["table"] is None:
    fc_filelist=os.path.normpath(processed_fc_filelist)
else:
    fc_filelist=os.path.normpath(args["table"])

if args["mounted"]:
    mountedir=os.path.normpath(args["mounted"])

if args["links"]:
    slinks_dir=os.path.normpath(args["links"])

#create directory for symlinks if it does not exist
if not os.path.isdir(os.path.normpath(slinks_dir)):
    os.mkdir(slinks_dir)


#get file names
if args["end"]:
    finalfcheck = args["end"]
if args["ini"]:
    inifcheck = args["ini"]


#difference in sizes
if args["difference"]:
    smalldif = args["difference"]
bottomr = 1 - smalldif
topr = 1 + smalldif


#get the time and date in the moment executed
timestamp = datetime.now()
print("\n\nrsyncPromethion %s is looking for local flowcell directories %s"%(version, timestamp))
now = "%04d-%02d-%02d_%02d:%02d:%02d"%(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second)


# check if mounted
warn_path = os.path.join(wpath, warning_msg)
alsowarn = os.path.join(homedir, warning_msg)
if os.path.isdir(os.path.join(os.path.normpath(mountedir), should_be_there)):
    if os.path.exists(warn_path):
        os.remove(warn_path)
        os.remove(alsowarn)
else:
    #If not mounted print warning ans save changes in local table
    with open(warn_path, 'a') as warn_file:
        warn_file.write(now +"\n")
    with open(alsowarn, 'a') as warn_file2:
        warn_file2.write(now +"\n")
    raise Exception("\n\nERROR!\n\nApparently /scratch is not mounted in %s\nTable will be NOT be updated and data will NOT be SYNCED.\n\n"%(mountedir))


# check if already running
if not args["force"]:
    warn_run = os.path.join(wpath, warning_flag)
    if os.path.exists(warn_run):
        raise Exception("\n\nAborting!\n%s file found, another instance of rsynPromethION could be runing.\n\n"%(warning_flag))





#open table with fc list and save each entry in a dictionary
processed_dirs = {}
with open(fc_filelist, 'r') as checkfile_list:
    #not using csv reader because I was having problems with empty lines
    for each_file in checkfile_list:
        if not each_file.strip():
            #ignore empty lines
            continue
        else:
            allcols =each_file.rstrip('\n').split(',')
            processed_dirs[allcols[0]] = [allcols[1], allcols[2], allcols[3], allcols[4]]


#check all directories in PromethION with the file that marks them as flowcells
print("Checking all exported flowcells...\n")
list_dirs = "find %s -name %s 2>/dev/null"%(wpath, inifcheck)
findout = os.popen(list_dirs).read()
dirs_findout=findout.split("\n")


#list flowcells in server that should be done
todemux_fc = set()
list_dirs = "find %s -name %s 2>/dev/null"%(mountedir, finalfcheck)
findout = os.popen(list_dirs).read()
scratch_fcs=findout.split("\n")
mountpath = mountedir + ".*"
for scratch_fc in scratch_fcs:
    #skip warnings from find command
    if (re.search(mountpath, scratch_fc)):
        fc_dir = scratch_fc.replace(mountedir, '')	#remove rest of path
        #print (fc_dir)
        todemux_fc.add(re.match(r'/(.+?)/(.*)', fc_dir).group(1))	#get only the first directory (NEED TO THINK OF A WAY TO DO THIS WITH os.path.split)



#compare directories with list of flowcells and sort which ones need to be updated
any_change = 0
parentdir = wpath + ".*"
for each_line in dirs_findout:
    #skip warnings from find command
    clean_dir = each_line
    if (re.search(parentdir, each_line)):
        clean_dir = each_line.replace(wpath, '')	#remove working directory from path
    else:
        continue
    if (re.search("^/\..*", clean_dir)):
        continue
    fc_name = re.match(r'/(.+?)/(.*)', clean_dir).group(1)	#get only the first directory (NEED TO THINK OF A WAY TO DO THIS WITH os.path.split)
    #print ("Checking %s"%(fc_name), end= " ")
    flowcell_parent = os.path.join(wpath, fc_name)
    #print(flowcell_parent)
    #check in dictionary if fc was processed already
    #print("%s: %s"%(processed_dirs[fc_name]))
    if ((fc_name in processed_dirs) and (processed_dirs[fc_name][2] != "Done")):
        flowcell_scratch = os.path.join(os.path.normpath(mountedir), fc_name)
        this_link = os.path.join(slinks_dir, fc_name)
        
        if not os.path.isdir(flowcell_scratch):
            print("+ %s was in %s but not found in server:"%(fc_name, fc_filelist), end=" ")
            #get size in local
            kilobytes = get_size(flowcell_parent)
            status = "new"
            serverkb = 0
            any_change = update_flowcell(fc_name, kilobytes, serverkb, status)
        else:
            #compare size in server and in local
            kilobytes = get_size(flowcell_parent)
            serverkb = get_size(flowcell_scratch)
            ratio = int(serverkb) / int(kilobytes)
            #print ("%s size in table is %s, is it in \"todemux\" set? %s"%(fc_name, int(processed_dirs[fc_name][0]),(fc_name in todemux_fc)))
            # check if flowcel finished and it is properly synced
            if ((kilobytes == int(processed_dirs[fc_name][0])) and (fc_name in todemux_fc) and (serverkb == int(processed_dirs[fc_name][1]))):
                #flowcell didn't change size in promethion, and includes the final summary in server.
                #print("Now checking %s difference in local size %s and server size %s. Ratio must be: %s > %s > %s"%(fc_name, kilobytes, serverkb, topr, ratio, bottomr))
                if ((ratio >= bottomr) and (ratio <= topr)):
                    #size of directories is similar in both server and promethion
                    print (">> %s finished and is already synced, setting it to \"Done\"."%(fc_name))
                    #update and remove links
                    status = "Done"
                    any_change = update_flowcell(fc_name, kilobytes, serverkb, status)
                elif (processed_dirs[fc_name][2] == "done?"):
                    print ("\nWarning! %s has been synced many times and seems done, but size difference with server did not decrease, ratio should be %s > %s > %s.\nTry running it next time with higher --difference."%(fc_name, topr, ratio, bottomr), end=" ")
                    status="done?"
                    any_change = update_flowcell(fc_name, kilobytes, serverkb, status)
                else:
                    print ("%s seems done, but size is different from server (size ratio: %s)."%(fc_name, ratio), end=" ")
                    status="done?"
                    any_change = update_flowcell(fc_name, kilobytes, serverkb, status)
                    
            else:
                #store new value
                status = "updated"
                any_change = update_flowcell(fc_name, kilobytes, serverkb, status)
            
    elif (fc_name not in processed_dirs):
        #save new directory with its size
        print ("++ New flowcell found.", end = " ")
        kilobytes = get_size(flowcell_parent)
        status = "new"
        serverkb = 0
        any_change = update_flowcell(fc_name, kilobytes, serverkb, status)



#sys.exit(0) #debug
# sync flowcells from sim links and table
if any_change == 1:
    #import pdb; pdb.set_trace()
    tosync = os.path.join(slinks_dir, "*")
    #execute this with os.system() OR os.popen()
    #fcsync = 'if mountpoint -q /network/mnt; then run-one rsync -L -avur --include="*/" --include=".md" --include="*.fast5" --include="*.fastq" --include="*.fastq.gz" --include="*pdf" --include="*js" --include="*txt" --include="*csv" --include="*html" --include="*json" --exclude="*" ' + tosync + ' ' + mountedir + ' >> /data/rsync.log 2>&1; fi'
    # CFL 2022/09/09 modify for cp bam and bam.bai files
    # CFL 2023/02/16 modify for copy fast5
    #fcsync = 'if mountpoint -q /network/mnt; then run-one rsync -L -avur --include="*/" --include=".md" --include="*.fast5" --include="*.pod5" --include="*.md" --include="*.fastq" --include="*.fastq.gz" --include="*pdf" --include="*js" --include="*txt" --include="*csv" --include="*html" --include="*json" --include="*bam" --include="*bam.bai" --exclude="*" ' + tosync + ' ' + mountedir + ' >> /data/rsync.log 2>&1; fi'
    #fcsync = 'if mountpoint -q %s; then run-one rsync -L -avur --include="*/" --include=".md" --include="*.fast5" --include="*.fastq" --include="*.fastq.gz" --include="*pdf" --include="*js" --include="*txt" --include="*csv" --include="*html" --include="*json" --exclude="*" ' + tosync + ' ' + mountedir + ' >> /data/rsync.log 2>&1; fi'
    # Cris 241219
    #fcsync = """if mountpoint -q %s; then run-one rsync -L -avur --no-o --no-g --no-perms --include="*/" --include=".md" --include="*.fast5" --include="*.pod5" --include="*.md" --include="*.fastq" --include="*.fastq.gz" --include="*pdf" --include="*js" --include="*txt" --include="*csv" --include="*html" --include="*json" --include="*bam" --include="*bam.bai" --exclude="*" %s  %s >> %s/rsync.log 2>&1; fi"""%(mountedir,tosync,mountedir,wpath)
    #create a file to stop the program if ran again while syncing
    #fcsync = """if mountpoint -q %s; then run-one rsync -avzP --omit-dir-times --no-o --no-g --no-perms --size-only %s %s >> %s/rsync.log 2>&1; fi"""%(mountedir,tosync,mountedir,wpath)
    #fcsync = """if [ ! -d %s]; then rsync -avzP --omit-dir-times --no-o --no-g --no-perms --size-only %s %s >> %s/rsync.log 2>&1; fi"""%(mountedir,tosync,mountedir,wpath)
    fcsync = """rsync -L -avurzP --omit-dir-times --no-o --no-g --no-perms --size-only %s %s >> %s/rsync.log 2>&1 """%(tosync,mountedir,wpath)
    #create a file to stop the program if ran again while syncing
    warn_run = os.path.join(wpath, warning_flag)
    with open(warn_run, 'a') as warn_file:
        warn_file.write(now)
    print ("\nNow rsyncing data to /scratch; this may take a while...", end =" ")
    if os.listdir(slinks_dir):
        # Cris 241219
        subprocess.call(fcsync, shell=True)
        #os.system(fcsync)
        print ("All flowcells synced.")
    else:
        print ("No flowcells to rsync.")
    # CFL 2023/12/18
    #os.system(fcsync)
    #rsync!
    #print(fcsync) ####DEBUG ONLY
    #update table with synced flowcells
    with open(fc_filelist, 'w') as fc_out:
        #sort flowcells by last element (date updated) and write them in the file
        for key, value in sorted(processed_dirs.items(), key=lambda x: x[1][3]):
            fc_out.write("%s,%s,%s,%s,%s\n"%(key, value[0], value[1], value[2], value[3]))
    #rsync the updated table so we know which directories we can move to the X directories to be analysed
    #tablesync = 'if mountpoint -q /network/mnt; then run-one rsync -vugpot ' + fc_filelist + ' ' + mountedir + '; fi'
    #tablesync = 'if mountpoint -q /home/prom/mount_isilon; then run-one rsync -vugpot ' + fc_filelist + ' ' + mountedir + '; fi'
    # Cris 241219
    #tablesync = """if mountpoint -q %s; then run-one rsync -vut --no-o --no-g --no-perms %s %s; fi"""%(mountedir,fc_filelist,mountedir)
    #tablesync = """if [ ! -d %s]; then rsync -avzP --omit-dir-times --no-o --no-g --no-perms --size-only %s %s; fi"""%(mountedir,fc_filelist,mountedir)
    tablesync = """rsync -vut --omit-dir-times --no-o --no-g --no-perms --size-only %s %s"""%(fc_filelist,mountedir)
    #execute this with os.system() OR os.popen()
    print ("Now syncing table to cluster")
    subprocess.call(tablesync, shell=True)
    #print(tablesync) ####DEBUG ONLY
    #remove the warning so program can be run again
    if os.path.exists(warn_run):
        os.remove(warn_run)
else:
    print ("No changes detected.")
print("\nAll done!\n-----------\n\n")
