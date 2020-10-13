#!/usr/bin/env python

#IMPORTANT! In order to trim the adapters, you need to specify the appropriate path to the adapter file, which might change between computers.

import os
import sys
import shutil
import argparse
import gzip
import glob
import re


R1 = glob.glob("*R1*.gz")
R2 = glob.glob("*R2*.gz")
prefixes=[re.sub(r'_.*','',reads1) for reads1 in R1]

R1.sort()
R2.sort()
prefixes.sort()

for (reads1,reads2,prefix) in zip (R1,R2,prefixes):
	print ("reads1: ", reads1, "; reads2: ", reads2, "prefixes: ", prefix)
	listToStr1 = ''.join(map(str, reads1))
	listToStr2 = ''.join(map(str, reads2))
	listToStr3 = ''.join(map(str, prefix))
	file = open("trim_prefixes.txt", "a")
	file.write("List of files \n R1 \n %s \n R2 \n %s \n Prefix \n %s \n ------------------- \n" % (listToStr1,listToStr2, listToStr3))
	file.close()
	os.system(r' trimmomatic PE -threads 4 -phred33 -trimlog logfile %s %s -baseout %s_filtered.fq.gz ILLUMINACLIP:/home/victor/miniconda3/envs/processing/share/trimmomatic-0.39-1/adapters/NexteraPE-PE.fa:2:30:10 SLIDINGWINDOW:15:30 MINLEN:36' % (reads1, reads2, prefix))

path = os.getcwd()
trim_dir = os.path.join(path, r'Trimmed')
os.mkdir(trim_dir)

path = os.getcwd()
paired_dir = os.path.join(trim_dir, r'Paired')
os.mkdir(paired_dir)

path = os.getcwd()
unpaired_dir = os.path.join(trim_dir, r'Unpaired')
os.mkdir(unpaired_dir)

for files in os.listdir(path):
	if files.endswith("P.fq.gz"):
		shutil.move(files,paired_dir)
	if files.endswith("U.fq.gz"):
		shutil.move(files,unpaired_dir)

os.chdir(paired_dir)
