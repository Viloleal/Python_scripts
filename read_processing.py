#!/usr/bin/env python

#preprocess read data

import os
import sys
import shutil
import argparse
import gzip
import glob
import re
import qcfunctions


path = os.getcwd()
print ("The current working directory is %s" % path)
fastq_check = len(glob.glob('*fastq.gz'))
print ("Evaluating number of Reads...")
print ("The cd contains %d files" % fastq_check)
#if fastq_check > 0:
#    fastq_check = True

# Check correct number of pairs...
pair_check = len(glob.glob('*_R*fastq.gz'))
if pair_check > 0:
	R1 = glob.glob('*_R1*fastq.gz')
	R1.sort()
	R2 = glob.glob('*_R2*fastq.gz')
	R2.sort()
	#print("<There are %d fastq files in this folder"%(fastq_check))
	if pair_check % 2 !=0:
		print ("Error! Paired files but unpair number of files. Check file list")
		exit()
	else:
		print("Creating file with list of reads at %s/read_list.txt" % path)		
		listToStr1 = ' '.join(map(str, R1))
		listToStr2 = ' '.join(map(str, R2))
		file = open("read_list.txt", "w")
		file.write("List of files \n %s \n \n %s" % (listToStr1,listToStr2))
		file.close()
		#print("R2: %s" % (R2))
else:
	print("Fastq files missing")

#Clumping files with clumpify (this will reduce file size un approx. 30%
print ("Clumping files with clumpify (this will reduce file size un approx. 30%")

qcfunctions.clump()

#Run Quality assessment using Fastqc and Multiqc (famuqc)
print ("Running quality assessment with Fastqc and Multiqc \n This may take some time...")

qcfunctions.famuqc()

print ("Running trimmomatic for adapter removal and read trimming")

qcfunctions.trim()

print ("Repeating QC analysis")

qcfunctions.famuqc()

