#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : createSampleCoverData_v0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : August 10 2016

import os
import re
import json
from __future__ import division
from BASE import read_bed
from BASE import clean_output

# CONFIG AREA #
path_bed = r'/Users/codeunsolved/Downloads/NGS-data/bed/onco-1606-probes.bed'
dir_depth_data = r'/Users/codeunsolved/Downloads/NGS-data/onco'
dir_output = r'/Users/codeunsolved/NGS/Topgen-Dashboard/data/onco'
depth_level = [20, 40, 60, 80, 100, 120, 140]


def output_sample_cover_data(data, sample_n, frag_n):
    pass


def init_sample_cover():
    sample_c = {"aver_depth": None, "max_depth": None, "min_depth": None, "frag_data": []}
    return sample_c


def init_frag_cover():
    frag_c = {}
    for f_key in frag_c:
        frag_c[f_key] = {"sample_name": "", "chr_num": re.match('chr(.+)', frag_details[f_key][0]).group(1),
                         "pos_s": frag_details[f_key][1], "pos_e": frag_details[f_key][2],
                         "gene_name": frag_details[f_key][3], "len": frag_details[f_key][2] - frag_details[f_key][1] + 1,
                         "aver_depth": None, "max_depth": None, "min_depth": None,
                         "depth": []}
    return frag_c


clean_output(dir_output, "sample_cover")
frag_details = read_bed(path_bed)
frag_details_sorted = sorted(frag_details.iteritems(), key=lambda d: (d[1]["chr_num"], d[1]["pos_s"]))

sample_num = 0
sample_data = []
for each_file in os.listdir(dir_depth_data):
    if re.match('^.+\.p-depth$', each_file):
        print "processing %s" % each_file
        sample_num += 1
        file_name = re.match('(.+)_S\d+_L\d+\.depth', each_file).group(1)
        with open(os.path.join(dir_depth_data, each_file), 'rb') as r_obj:
            sample_data.append(init_sample_cover())
            depth_level_counts = {}
            for line_depth in r_obj:
                chr_n = re.match('([^\t]+)\t', line_depth).group(1)
                pos = int(re.match('[^\t]+\t([^\t]+\t)', line_depth).group(1))
                depth = int(re.match('(?:[^\t]+\t){2}([^\t\n\r]+)', line_depth).group(1))
                for key, value in frag_details_sorted:
                    sample_data[-1]["frag_data"].append({"key": key, "frag_cover": init_frag_cover()})
                    frag_cover = sample_data[-1]["frag_data"][-1]["frag_cover"]
                    frag_cover["sample_name"] = file_name
                    if key not in depth_level_counts:
                        depth_level_counts[key] = {}
                        for each_depth_level in depth_level:
                            depth_level_counts[key][each_depth_level] = 0
                    frag_cover["depth"].append({"pos": pos, "depth": depth})
                    for each_depth_level in depth_level:
                        if depth >= each_depth_level:
                            depth_level_counts[key][each_depth_level] += 1
            for each_frag in sample_data[-1]["frag_data"]:


