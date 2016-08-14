#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : createSampleCoverData_v0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : August 10 2016

from __future__ import division
import os
import re
import json
from BASE import read_bed
from BASE import clean_output

# CONFIG AREA #
path_bed = r'/Users/codeunsolved/Downloads/NGS-data/bed/onco-1606-probes.bed'
dir_depth_data = r'/Users/codeunsolved/Downloads/NGS-data/onco'
dir_output = r'/Users/codeunsolved/NGS/Topgen-Dashboard/data/onco'
depth_level = [20, 50, 100, 200, 500, 1000]


def output_sample_cover_data(data, sample_n, frag_n):
    pass


def init_sample_data_pointer():
    sample_d = {"aver_depth": None, "max_depth": None, "min_depth": None, "frag_cover": []}
    return sample_d


def init_frag_data():
    frag_d = {}
    for f_key in frag_details:
        frag_d[f_key] = {"sample_name": "", "chr_num": re.match('chr(.+)', frag_details[f_key][0]).group(1),
                         "pos_s": frag_details[f_key][1], "pos_e": frag_details[f_key][2],
                         "gene_name": frag_details[f_key][3],
                         "len": frag_details[f_key][2] - frag_details[f_key][1] + 1,
                         "aver_depth": None, "max_depth": None, "min_depth": None,
                         "x_label": [], "depth": []}
    return frag_d


clean_output(dir_output, "sample_cover")
frag_details = read_bed(path_bed)
frag_details_sorted = sorted(frag_details.iteritems(), key=lambda d: (d[1][0], d[1][1]))

sample_num = 0
sample_cover = []
for each_file in os.listdir(dir_depth_data):
    if re.match('^.+\.p-depth$', each_file):
        print "processing %s..." % each_file
        sample_num += 1
        file_name = re.match('(.+)_S\d+_L\d+\.depth', each_file).group(1)
        with open(os.path.join(dir_depth_data, each_file), 'rb') as r_obj:
            sample_cover.append({"sdp": init_sample_data_pointer()})
            depth_level_counts = {}
            depth_stat = {"sample": {"sum": 0, "max": None, "min": None}}
            for line_depth in r_obj:
                chr_n = re.match('([^\t]+)\t', line_depth).group(1)
                pos = int(re.match('[^\t]+\t([^\t]+\t)', line_depth).group(1))
                depth = int(re.match('(?:[^\t]+\t){2}([^\t\n\r]+)', line_depth).group(1))
                for key, value in frag_details_sorted:
                    sample_cover[-1]["sdp"]["frag_cover"].append({"key": key, "frag_data": init_frag_data()})
                    frag_data = sample_cover[-1]["sdp"]["frag_cover"][-1]["frag_data"]
                    frag_data["sample_name"] = file_name
                    # init depth_level_counts[key]
                    if key not in depth_level_counts:
                        depth_level_counts[key] = {}
                        for each_depth_level in depth_level:
                            depth_level_counts[key][each_depth_level] = 0
                    # init depth_stat[key]
                    if key not in depth_stat:
                        depth_stat[key] = {"sum": 0, "max": None, "min": None}
                    # count depth_level_counts[key]
                    for each_depth_level in depth_level:
                        if depth >= each_depth_level:
                            depth_level_counts[key][str(each_depth_level)] += 1
                    # count depth_stat sum
                    depth_stat["sample"]["sum"] += depth
                    depth_stat[key]["sum"] += depth
                    # count depth_stat max
                    if depth > depth_stat["sample"]["max"] or depth_stat["sample"]["max"] is None:
                        depth_stat["sample"]["max"] = depth
                    if depth > depth_stat[key]["max"] or depth_stat[key]["max"] is None:
                        depth_stat[key]["max"] = depth
                    # count depth_stat min
                    if depth < depth_stat["sample"]["min"] or depth_stat["sample"]["min"] is None:
                        depth_stat["sample"]["min"] = depth
                    if depth < depth_stat[key]["min"] or depth_stat[key]["min"] is None:
                        depth_stat[key]["min"] = depth
                    # add x_label and depth
                    frag_data["x_label"].append(pos)
                    frag_data["depth"].append(depth)
            depth_level_stat_sample = {"total_len": 0}
            for each_frag in sample_cover[-1]["sdp"]["frag_cover"]:
                key = each_frag["key"]
                for each_depth_level in depth_level:
                    if each_depth_level not in depth_level_stat_sample:
                        depth_level_stat_sample[str(each_depth_level)] = 0
                    each_frag[each_depth_level] = round(
                        depth_level_counts[key][str(each_depth_level)] / len(each_frag["frag_data"]["x_label"]), 2)
                    depth_level_stat_sample["total_len"] += len(each_frag["frag_data"]["x_label"])
                    depth_level_stat_sample[str(each_depth_level)] += depth_level_counts[key][str(each_depth_level)]
            for each_depth_level in depth_level:
                sample_cover[-1][each_depth_level] = round(
                    depth_level_stat_sample[str(each_depth_level)] / depth_level_stat_sample["total_len"], 2)

output_sample_cover_data(sample_cover, sample_num, len(frag_details))
