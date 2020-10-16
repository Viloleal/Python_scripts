#!/usr/bin/env python

import numpy as np
import pandas as pd
import os
import sys
import shutil
import argparse
import gzip
import glob
import re
import subprocess


#Extracting headers from vcfs

vcfs = glob.glob("*vcf.gz")
prefixes = [re.sub(r'.sim.vcf.gz','',vcf) for vcf in vcfs]
vcfs.sort()
prefixes.sort()
path = os.getcwd()

prox_dir = os.path.join(path, r'Proximal')
head_dir = os.path.join(path, r'Headers')
os.mkdir(prox_dir)
os.mkdir(head_dir)

for (files,prefix) in zip (vcfs,prefixes):
	print ("vcf: ", files, "; prefix: ", prefix)
	listToStr1 = ''.join(map(str, files))
	listToStr2 = ''.join(map(str, prefix))
	file = open("vcfs_prefixes.txt", "a")
	file.write("List of files \n vcfs \n %s \n Prefix \n %s \n ------------------- \n" % (listToStr1,listToStr2))
	file.close()
	subprocess.call(['bash', '-c', 'bcftools view -h %s >> %s.header.txt' % (files, prefix)])
	subprocess.call(['bash', '-c', 'bcftools view --no-header %s -O v -o %s.nohead.vcf' % (files, prefix)])
	for files in os.listdir(path):
		if files.endswith("header.txt"):
			shutil.copy(files,prox_dir)
			shutil.copy(files,head_dir)
		if files.endswith("nohead.vcf"):
			shutil.move(files,prox_dir)	
		headers = glob.glob("*header.txt")
		headers.sort()


for header in headers:
	header_dir = os.path.join(path, '%s' % (header))
	print("Removing header files...")
	print(header_dir)
	os.remove(header_dir) 	
	 
	os.chdir(prox_dir)

#removing snps within 10 bp from each other

vcfs = glob.glob("*nohead.vcf")
prefixes=[re.sub(r'.nohead.vcf','',vcf) for vcf in vcfs]
vcfs.sort()
prefixes.sort()

def prox(dist):
    ex=[]
    remove = pd.DataFrame(columns=["Pos1", "Pos2", "Pos3"])
    for i in range(len(df2)-1):
        #print (r.pos)
        a=df2.loc[i].pos
        b=df2.loc[i+1].pos
        if b-a<=dist:
            #print (a,b, a-b)
            ex.extend([a,b])
            d = pd.DataFrame({"Pos1":[a], "Pos2":[b], "Pos3":[b-a]})
            remove = remove.append(d)
    #print (ex)
    return df2[~df2.pos.isin(ex)], remove



path = os.getcwd()

for (files,prefix) in zip (vcfs,prefixes):
	print ("vcf: ", files, "; prefix: ", prefix)
	listToStr1 = ''.join(map(str, files))
	listToStr2 = ''.join(map(str, prefix))
	file = open("vcfs_prefixes1.txt", "a")
	file.write("List of files \n vcfs \n %s \n Prefix \n %s \n ------------------- \n" % (listToStr1,listToStr2))
	file.close()
	df1 = pd.read_table('%s.nohead.vcf' % (prefix), names=['chrom','pos','a','b','c','d','e','f'], index_col=False)
	df2 = df1[df1.b != 'N'] 
	dfx, remove = prox(10)
	print ("Removed %s positions" % (len(df2)-len(dfx)))
	dfx.to_csv('%s_processed.vcf' % (prefix), sep = '\t', header=False, index=False)
	remove.to_csv('%s_removed.vcf' % (prefix), header=True,index=False)

#Changing headers to vcf files

vcfs = glob.glob("*_processed.vcf")
prefixes=[re.sub(r'.processed.vcf','',vcf) for vcf in vcfs]
headers = glob.glob("*header.txt")
vcfs.sort()
prefixes.sort()
headers.sort()

for (files,prefix,header) in zip (vcfs,prefixes,headers):
	print ("vcf: ", files, "; prefix: ", prefix, "header: ", header)
	listToStr1 = ''.join(map(str, files))
	listToStr2 = ''.join(map(str, prefix))
	listToStr3 = ''.join(map(str, header))
	file = open("vcfs_prefixes2.txt", "a")
	file.write("List of files \n vcfs \n %s \n Prefix \n %s \n Header \n %s \n ------------------- \n" % (listToStr1,listToStr2, listToStr3))
	file.close()
	subprocess.call(['bash', '-c', 'cat %s %s >> %s.processed_zc.vcf' % (header, files, prefix)]) 

#move files to their corresponding directories

path = os.getcwd()
rem_dir = os.path.join(path, r'Removed_positions')
os.mkdir(rem_dir)

proc_dir = os.path.join(path, r'Processed_vcfs')
os.mkdir(proc_dir)

for files in os.listdir(path):
	if files.endswith("processed.vcf"):
		shutil.move(files,proc_dir)
	if files.endswith("removed.vcf"):
		shutil.move(files,rem_dir)
for header in headers:
	header_dir = os.path.join(path, '%s' % (header))
	print("Removing header files...")
	print(header_dir)
	os.remove(header_dir)
