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
prefixes = [re.sub(r'_.*','',vcf) for vcf in vcfs]
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


for header in headers:
	header_dir = os.path.join(path, '%s' % (header))
	print("Removing header files...")
	print(header_dir)
	os.remove(header_dir) 	
	 
	os.chdir(prox_dir)

#removing snps within 10 bp from each other

vcfs = glob.glob("*nohead.vcf")
prefixes=[re.sub(r'_.*','',vcf) for vcf in vcfs]
vcfs.sort()
prefixes.sort()

def prox(i):
    rows = df2.shape[0]
    while i < rows: #quito el igual
    	y = i 
    	if y == rows-1: #cambio y >= rows por y == rows-1 para que cuando el bucle entre en la ultima fila se pare (ya que no puedes añadir un campo diff en la siguiente, porque no existe, y aparece el error de "out of bounds") 
    		pass
    		i+=1 #sumo 1 para que finalice el bucle while una vez entremos en esta condición. Si no sumas 1 el while se convierte en un bucle infinito.
    	else:
	        y = i + 1
	        di = df2.iloc[i,1]
	        dy = df2.iloc[y,1]
	        diff = np.subtract(dy, di)
	        #print(diff)
	        df2.loc[df2.index[y], 'DIFF'] = diff
	        i = i + 1

path = os.getcwd()

for (files,prefix) in zip (vcfs,prefixes):
	print ("vcf: ", files, "; prefix: ", prefix)
	listToStr1 = ''.join(map(str, files))
	listToStr2 = ''.join(map(str, prefix))
	file = open("vcfs_prefixes1.txt", "a")
	file.write("List of files \n vcfs \n %s \n Prefix \n %s \n ------------------- \n" % (listToStr1,listToStr2))
	file.close()
	df1 = pd.read_table('%s/%s' % (path,files), header = None) 
	df2 = df1[df1[3] != 'N'] 
	prox(0)
	df10 = df2.loc[df2['DIFF'] <= 10]
	df2 = df2.drop(df2[df2.DIFF <=10].index)
	dfn = df1.loc[df1[3] == 'N']
	df = pd.concat([df2,dfn])
	df = df.drop(['DIFF'], axis=1)
	df = df.sort_index(axis=0)
	df.to_csv('%s_proc.vcf' % (prefix), sep = '\t', header=False, index=False)
	df10.to_csv('%s_proc.10.vcf' % (prefix), sep = '\t', header=False, index=False)

#Changing headers to vcf files

vcfs = glob.glob("*_proc.vcf")
prefixes=[re.sub(r'_.*','',vcf) for vcf in vcfs]
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
	if files.endswith("processed_zc.vcf"):
		shutil.move(files,proc_dir)
	if files.endswith("_proc.10.vcf"):
		shutil.move(files,rem_dir)
for header in headers:
	header_dir = os.path.join(path, '%s' % (header))
	print("Removing header files...")
	print(header_dir)
	os.remove(header_dir)
