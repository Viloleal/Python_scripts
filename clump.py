#!/usr/bin/env python

import os
import sys
import shutil
import argparse
import gzip
import glob
import re

#Clump reads using clumpify
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
	file = open("reads_prefixes.txt", "a")
	file.write("List of files \n R1 \n %s \n R2 \n %s \n Prefix \n %s \n ------------------- \n" % (listToStr1,listToStr2, listToStr3))
	file.close()
	os.system(r' clumpify.sh -Xmx1g in=%s in2=%s out1=%s_R1_clumped.fastq.gz out2=%s_R2_clumped.fastq.gz' % (reads1, reads2, prefix, prefix))

path = os.getcwd()
clump_dir = os.path.join(path, r'clumped')
os.mkdir(clump_dir)
for files in os.listdir(path):
	if files.endswith("clumped.fastq.gz"):
		shutil.move(files,clump_dir)
os.chdir(clump_dir)




