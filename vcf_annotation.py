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
prefixes=[re.sub(r'.vcf','',vcf) for vcf in vcfs]
vcfs.sort()
prefixes.sort()
for (files,prefix) in zip (vcfs,prefixes):
	print ("vcf: ", files, "; prefix: ", prefix)
	listToStr1 = ''.join(map(str, files))
	listToStr2 = ''.join(map(str, prefix))
	file = open("vcfs_prefixes.txt", "a")
	file.write("List of files \n vcfs \n %s \n Prefix \n %s \n ------------------- \n" % (listToStr1,listToStr2))
	file.close()
	subprocess.call(['bash', '-c', ' ~/bin/snpEff_latest_core/snpEff/scripts/snpEff -v Mycobacterium_bovis_af2122_NC002945.4 %s -ud 0 >> %s_ann.vcf' % (files, prefix)])
path = os.getcwd()
ann_dir = os.path.join(path, r'Annotations')
os.mkdir(ann_dir)
