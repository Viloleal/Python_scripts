#!/usr/bin/env python
#Batch SNP simulation from vcf files
#OBS! Long fasta headers (>) in the reference sequence can give rise to errors. It is convenient to reduce header size to minimum when using guided SNP simulation

import os
import sys
import shutil
import argparse
import gzip
import glob
import re

path = os.getcwd()

print ("The current working directory is %s" % path)
vcf_check = len(glob.glob("*.vcf*"))
print ("Evaluating number of vcf files...")
print ("Searching for reference genome...")

if vcf_check < 1:
	print ("Error! No vcf files available in current directory" )
else:
	vcf=glob.glob("*vcf*")
	prefixes=[re.sub(r'.vcf.*','',files) for files in vcf]
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
		os.system(r' simuG.pl -refseq NC_002945v4_modified.fasta -snp_vcf %s -prefix %s ' % (files, prefix))
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
	
