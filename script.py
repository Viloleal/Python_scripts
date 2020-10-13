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

vcfs = glob.glob("*vcf*")
prefixes = [re.sub(r'.vcf.gz','',vcf) for vcf in vcfs]
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
	subprocess.call(['bash', '-c', 'bcftools view --no-header %s >> %s.nohead.vcf' % (files, prefix)])
	for files in os.listdir(path):
		if files.endswith("header.txt"):
			shutil.copy(files,prox_dir)
			shutil.copy(files,head_dir)
		if files.endswith("nohead.vcf"):
			shutil.move(files,prox_dir)	
		headers = glob.glob("*header.txt")
		headers.sort()

vcfs = glob.glob("*vcf*")
prefixes = [re.sub(r'.nohead.vcf','',vcf) for vcf in vcfs]
vcfs.sort()
prefixes.sort()
path = os.getcwd()

for (files,prefix) in zip (vcfs,prefixes):
	print ("vcf: ", files, "; prefix: ", prefix)
	listToStr1 = ''.join(map(str, files))
	listToStr2 = ''.join(map(str, prefix))
	file = open("vcfs_prefixes.txt", "a")
	file.write("List of files \n vcfs \n %s \n Prefix \n %s \n ------------------- \n" % (listToStr1,listToStr2))
	file.close()
	df1 = pd.read_table('%s/%s' % (path,files), header = None)
	df1[0] = df1[0].str.replace('LT708304.1','NC_002945.4')
	df1.to_csv('%s_proc.vcf' % (prefix), sep = '\t', header=False, index=False)

vcfs = glob.glob("*_proc.vcf")
prefixes=[re.sub(r'_proc.vcf','',vcf) for vcf in vcfs]
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


bcftools view -e 'ALT =="."' 13-11594_2.renamed.vcf.gz -o 13-11594_2.filt.vcf.gz -O z

#HAY QUE QUITAR LT708304.1 TMB DEL HEADER. 
sed -i 's/LT708304.1/NC_002945.4/g' 13-11594_2.vcf #<<-- DE HECHO ESTO ES MUCHO MAS RAPIDO QUE TODO LO ANTERIOR
