#!/usr/bin/env python

import argparse
import os
import sys
import shutil
import argparse
import gzip
import glob
import re

parser = argparse.ArgumentParser(description="Batch SNP simulation from vcf files")
parser.add_argument("Reference", metavar = "-R", type=str, help ="reference genome in .fasta format")
args = parser.parse_args()

ref = args.Reference
print(ref)

path = os.getcwd()

print ("The current working directory is %s" % path)
vcf_check = len(glob.glob("*.vcf*"))
print ("Evaluating number of vcf files...")
print ("Searching for reference genome...")

if vcf_check < 1:
	print ("Error! No vcf files available in current directory" )
else:
	vcf=glob.glob("*vcf.gz")
	prefixes=[re.sub(r'.filt.vcf.gz','',files) for files in vcf]
	vcf.sort()
	prefixes.sort()
	print("The cd contains %s files\nCreating file with list of vcfs at %s" % (vcf_check, path))
	file = open("vcfs.txt", "a")
	file.write("List of files \n") 	
	for (files,prefix) in zip (vcf,prefixes):
		listToStr1 = ''.join(map(str, files))	
		listToStr2 = ''.join(map(str, prefix))
		file.write(" File \n %s \n Prefix \n %s \n ------------------- \n" % (listToStr1,listToStr2))
		file.close
		os.system(r' simuG.pl -refseq %s -snp_vcf %s -prefix %s ' % (ref, files, prefix))
	sim = os.path.join(path, r'Simulations')
	os.mkdir(sim)
	for files in os.listdir(path):
		if files.endswith("genome.fa"):
			shutil.move(files,sim)
	for files in os.listdir(path):
		if files.endswith("map.txt"):
			shutil.move(files,sim)
	for files in os.listdir(path):
		if files.endswith("SNP.vcf"):
			shutil.move(files,sim)
	
