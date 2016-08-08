#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : createAmpliconData_v0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : August 8 2016

import os
import re
import shutil
import json

# CONFIG AREA #
path_bed = r'/Users/codeunsolved/Downloads/NGS-data/bed/BRAC-1606-2.bed'
dir_depth_data = r'/Users/codeunsolved/Downloads/NGS-data/BRAC160322-2'
dir_output = r'/Users/codeunsolved/NGS/Topgen-Dashboard/data/BRAC160322'


def read_bed(path_b):
    a_details = {}
    with open(path_b, 'rb') as r_obj_b:
        for line_no, line_b in enumerate(r_obj_b):
            if line_no > 0:
                chr_n = re.match('([^\t]+)\t', line_b).group(1)
                pos_s = int(re.match('[^\t]+\t([^\t]+\t)', line_b).group(1))
                pos_e = int(re.match('(?:[^\t]+\t){2}([^\t]+\t)', line_b).group(1))
                gene_name = re.match('(?:[^\t]+\t){3}([^\t\n\r]+)', line_b).group(1)
                if re.search('[:\-_]', gene_name):
                    gene_name = ' '
                a_details["%s-%s-%s" % (chr_n, gene_name, pos_s)] = [chr_n, pos_s, pos_e, gene_name]
    return a_details


def clean_output():
    if os.path.isdir(os.path.join(dir_output, "amplicon")):
        shutil.rmtree(os.path.join(dir_output, "amplicon"))
    os.mkdir(os.path.join(dir_output, "amplicon"))


def output_amplicon_data(data, sample_n, amplicon_n):
    data_pointer = {"sample_num": sample_n, "amplicon_num": amplicon_n,
                    "amplicon_data": []}
    data_sorted = sorted(data.iteritems(), key=lambda d: (d[1]["chr_num"], d[1]["pos_s"]))
    for key, value in data_sorted:
        path_amplicon_depth = "data/%s/amplicon/%s" % (os.path.basename(dir_output), key)
        with open(os.path.join(os.path.join(dir_output, "amplicon"), "%s.json" % key), 'wb') as w_obj:
            w_obj.write(json.dumps(value))
            data_pointer["amplicon_data"].append({"name": value["gene_name"], "path": path_amplicon_depth,
                                                  "pass": value["pass"], "failed": value["failed"]})
    with open(os.path.join(os.path.join(dir_output, "amplicon"), "data_pointer.json"), 'wb') as w_obj:
        w_obj.write(json.dumps(data_pointer))


clean_output()
amplicon_details = read_bed(path_bed)

amplicon_data = {}
for key in amplicon_details:
    amplicon_data[key] = {"depth": {}, "chr_num": re.match('chr(.+)', amplicon_details[key][0]).group(1),
                          "pos_s": amplicon_details[key][1], "pos_e": amplicon_details[key][2],
                          "gene_name": amplicon_details[key][3],
                          "len": amplicon_details[key][2] - amplicon_details[key][1] + 1,
                          "pass": 0, "failed": 0}

sample_num = 0
for each_file in os.listdir(dir_depth_data):
    if re.match('.+\.depth$', each_file):
        print "processing %s..." % each_file
        sample_num += 1
        file_name = re.match('(.+)_S\d+_L\d+\.depth', each_file).group(1)
        with open(os.path.join(dir_depth_data, each_file), 'rb') as r_obj:
            pass_dict = {}
            for line_depth in r_obj:
                chr_n = re.match('([^\t]+)\t', line_depth).group(1)
                pos = int(re.match('[^\t]+\t([^\t]+\t)', line_depth).group(1))
                depth = int(re.match('(?:[^\t]+\t){2}([^\t\n\r]+)', line_depth).group(1))
                for key in amplicon_details:
                    if file_name not in amplicon_data[key]["depth"]:
                        amplicon_data[key]["depth"][file_name] = []
                    if key not in pass_dict:
                        pass_dict[key] = 1
                    if chr_n == amplicon_details[key][0] and \
                                            amplicon_details[key][1] <= pos <= amplicon_details[key][2]:
                        amplicon_data[key]["depth"][file_name].append({"pos": pos, "depth": depth})
                        # print "add %s" % {"pos": pos, "depth": depth}
                        if depth < 10:
                            pass_dict[key] = 0
            for pass_key in pass_dict:
                if pass_dict[pass_key] == 0:
                    amplicon_data[pass_key]["failed"] += 1
                else:
                    amplicon_data[pass_key]["pass"] += 1

output_amplicon_data(amplicon_data, sample_num, len(amplicon_details))
