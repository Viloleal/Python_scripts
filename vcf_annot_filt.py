#!/usr/bin/env python

import os
import sys
import shutil
import argparse
import gzip
import glob
import re
import subprocess

vcfs = glob.glob("*.vcf")
prefixes=[re.sub(r'_.*','',vcf) for vcf in vcfs]
vcfs.sort()
prefixes.sort()
for (files,prefix) in zip (vcfs,prefixes):
	print ("vcf: ", files, "; prefix: ", prefix)
	listToStr1 = ''.join(map(str, files))
	listToStr2 = ''.join(map(str, prefix))
	file = open("vcfs_prefixes.txt", "a")
	file.write("List of files \n vcfs \n %s \n Prefix \n %s \n ------------------- \n" % (listToStr1,listToStr2))
	file.close()
	subprocess.call(['bash', '-c', ' ~/bin/snpEff_latest_core/snpEff/scripts/snpEff -v Mycobacterium_bovis_af2122_NC002945.4 %s -ud 0 >> %s_SNP.ann.vcf' % (files, prefix)])
path = os.getcwd()
ann_dir = os.path.join(path, r'Annotations')
os.mkdir(ann_dir)

filt_dir = os.path.join(path, r'Filtered_out')
os.mkdir(filt_dir)
remain_dir = os.path.join(path, r'Remaining')
os.mkdir(remain_dir)

ann = glob.glob("*ann.vcf")
prefixes_ann = [re.sub(r'_.*','',annotations) for annotations in ann]
ann.sort()
prefixes_ann.sort()
for (annotations,prefix) in zip (ann,prefixes_ann):
	print ("annotations: ", annotations, "; prefixes: ", prefix)
	listToStr1 = ''.join(map(str,annotations))
	listToStr2 = ''.join(map(str,prefix))
	file = open("ann_prefixes.txt", "a")
	file.write("List of files \n Annotation_files \n %s \n Prefix_files \n %s \n ------------------- \n" % (listToStr1,listToStr2))
	file.close()
	subprocess.call(['bash', '-c', ' java -jar ~/bin/snpEff_latest_core/snpEff/SnpSift.jar filter \"((ANN[*].GENE =~ \'PE\') | (ANN[*].GENE =~ \'transposase\')) & (ANN[*].EFFECT != \'intergenic_region\')\" %s > ./Filtered_out/%s_SNP.ann.filt.vcf' % (annotations, prefix)])
	subprocess.call(['bash', '-c', ' java -jar ~/bin/snpEff_latest_core/snpEff/SnpSift.jar filter -n \"((ANN[*].GENE =~ \'PE\') | (ANN[*].GENE =~ \'transposase\')) & (ANN[*].EFFECT != \'intergenic_region\')\" %s > ./Filtered_out/%s_SNP.ann.rem.vcf' % (annotations, prefix)])
for files in os.listdir(path):
	if files.endswith("ann.vcf"):
		shutil.move(files,ann_dir)
	if files.endswith("ann.filt.vcf"):
		shutil.move(files,filt_dir)
	if files.endswith("ann.rem.vcf"):
		shutil.move(files,remain_dir)
