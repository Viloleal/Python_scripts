#!/usr/bin/env python

import argparse
import os
import sys
import shutil
import gzip
import glob
import re
import subprocess
import som

truths=glob.glob("*filt*")
queries=glob.glob("*sim*")

truths.sort()
queries.sort()

prefixes=[re.sub(r'.filt.vcf.gz','',truth) for truth in truths]
prefixes.sort()


for (truth,query,prefix) in zip (truths,queries,prefixes):
	print ("Truth vcfs: ", truth, "; Query vcfs: ", query, "Prefix: ", prefix)
	listToStr1 = ''.join(map(str, truth))
	listToStr2 = ''.join(map(str, query))
	listToStr3 = ''.join(map(str, prefix))
	file = open("vcfs_prefixes2.txt", "a")
	file.write("List of files \n Truth vcfs \n %s \n Query vcfs \n %s \n Prefixr \n %s \n ------------------- \n" % (listToStr1,listToStr2, listToStr3))
	file.close()
	subprocess.call(['python', 'som.py -r ~/miniconda3/envs/ame/dependencies/vSNP_reference_options/Mycobacterium_AF2122/NC_002945v4.fasta %s %s -o %s_comparison ' % (truth, query, prefix)])


