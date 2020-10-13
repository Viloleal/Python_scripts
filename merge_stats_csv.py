#!/usr/bin/env python

import pandas as pd
import numpy as np
import glob
import re

csvs = glob.glob('*.csv')
csvs
prefixes = [re.sub(r'.stats.csv','',files) for files in csvs]
csvs.sort()
prefixes.sort()

for (files,prefix) in zip(csvs,prefixes):
    df = pd.read_csv('%s' % (files))
    df.insert(0, "Name", ['%s' % (prefix),'%s' % (prefix),'%s' % (prefix)], True)
    df2 = pd.DataFrame(df)
    df2.to_csv('%s.stats_2.csv' % (prefix), index = False)

df3 = pd.concat([pd.read_csv(f) for f in glob.glob('*stats_2.csv')], ignore_index = True)
df3.to_csv('merged_stats.csv', index = False)


