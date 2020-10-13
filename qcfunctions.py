#!/usr/bin/env python

import os
import sys
import shutil
import argparse
import gzip
import glob
import re

#Clump reads using clumpify
def clump():
	R1 = glob.glob("*_R1*.gz")
	R2 = glob.glob("*_R2*.gz")
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
		os.system(r' clumpify.sh -Xmx8g in=%s in2=%s out1=%s_R1_clumped.fastq.gz out2=%s_R2_clumped.fastq.gz' % (reads1, reads2, prefix, prefix))

	path = os.getcwd()
	clump_dir = os.path.join(path, r'clumped')
	os.mkdir(clump_dir)
	for files in os.listdir(path):
		if files.endswith("clumped.fastq.gz"):
			shutil.move(files,clump_dir)
	os.chdir(clump_dir)

# QUALITY CONTROL EVALUATION USING FASTQC & MULTIQC (famuqc)
def famuqc():
	print("Initiating Read quality evaluation through Fastqc")
	list_of_files = glob.glob("*.gz")	
	path = os.getcwd()	
	fastqcdir = os.path.join(path, r'fastqc')
	try:
		os.mkdir(fastqcdir)
	except OSError:
		print ("Creation of the directory for fastqc failed")
	else:
		print ("Successfully created the directory for fastqc at %s" % fastqcdir)

	for afile in list_of_files:
		os.system(r'fastqc -t 4 -o ./fastqc %s' % afile)

	multiqcdir = os.path.join(path, r'multiqc')
	try:
		os.mkdir(multiqcdir)
	except OSError:
		print ("Creation of the directory for multiqc failed")
	else:
		print ("Successfully created the directory for multiqc at %s" % multiqcdir)

	os.chdir(fastqcdir)
	os.system(r' multiqc ./ -o ../multiqc --interactive')
	os.chdir(path)

	print("Removing fastqc output files...")
	shutil.rmtree(fastqcdir)

def trim():
	R1 = glob.glob("*_R1*.gz")
	R2 = glob.glob("*_R2*.gz")
	prefixes=[re.sub(r'_.*','',reads1) for reads1 in R1]

	R1.sort()
	R2.sort()
	prefixes.sort()

	path = os.getcwd()
	trim_dir = os.path.join(path, r'Trimmed')
	os.mkdir(trim_dir)

	#path = os.getcwd()
	paired_dir = os.path.join(trim_dir, r'Paired')
	os.mkdir(paired_dir)

	#path = os.getcwd()
	unpaired_dir = os.path.join(trim_dir, r'Unpaired')
	os.mkdir(unpaired_dir)

	for (reads1,reads2,prefix) in zip (R1,R2,prefixes):
		print ("reads1: ", reads1, "; reads2: ", reads2, "prefixes: ", prefix)
		listToStr1 = ''.join(map(str, reads1))
		listToStr2 = ''.join(map(str, reads2))
		listToStr3 = ''.join(map(str, prefix))
		file = open("trim_prefixes.txt", "a")
		file.write("List of files \n R1 \n %s \n R2 \n %s \n Prefix \n %s \n ------------------- \n" % (listToStr1,listToStr2, listToStr3))
		file.close()
		os.system(r' trimmomatic PE -threads 4 -phred33 -trimlog logfile %s %s -baseout %s_filtered.fq.gz ILLUMINACLIP:/home/victor/miniconda3/envs/processing/share/trimmomatic-0.39-1/adapters/NexteraPE-PE.fa:2:30:10 SLIDINGWINDOW:15:30 MINLEN:36' % (reads1, reads2, prefix))


	for files in os.listdir(path):
		if files.endswith("P.fq.gz"):
			shutil.move(files,paired_dir)
		if files.endswith("U.fq.gz"):
			shutil.move(files,unpaired_dir)

	os.chdir(paired_dir)


