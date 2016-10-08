#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : create_amplicon_data
# AUTHOR  : codeunsolved@gmail.com
# CREATED : August 8 2016
# VERSION : v0.0.1a

import os
import re
import sys
import json

from base import read_bed
from base import clean_output

# CONFIG AREA #
dir_depth_data = sys.argv[1]
path_bed = sys.argv[2]
dir_output = sys.argv[3]


def output_amplicon_data(data, sample_n, amplicon_n):
    data_pointer = {"sample_num": sample_n, "amplicon_num": amplicon_n,
                    "amplicon_data": []}
    data_sorted = sorted(data.iteritems(), key=lambda d: (d[1][0], d[1][1]))
    for d_key, d_value in data_sorted:
        path_amplicon_depth = "data/%s/amplicon/%s.json" % (os.path.basename(dir_output), d_key)
        with open(os.path.join(os.path.join(dir_output, "amplicon"), "%s.json" % d_key), 'wb') as o_amplicon:
            o_amplicon.write(json.dumps(d_value))
            data_pointer["amplicon_data"].append({"name": d_value["gene_name"], "path": path_amplicon_depth,
                                                  "pass": d_value["pass"], "failed": d_value["failed"]})
    with open(os.path.join(os.path.join(dir_output, "amplicon"), "data_pointer.json"), 'wb') as o_dp:
        o_dp.write(json.dumps(data_pointer))


def init_amplicon_data():
    amplicon_d = {}
    for a_key in amplicon_details:
        amplicon_d[a_key] = {"depth": {}, "chr_num": re.match('chr(.+)', amplicon_details[a_key][0]).group(1),
                             "pos_s": amplicon_details[a_key][1], "pos_e": amplicon_details[a_key][2],
                             "gene_name": amplicon_details[a_key][3],
                             "len": amplicon_details[a_key][2] - amplicon_details[a_key][1] + 1,
                             "pass": 0, "failed": 0}
    return amplicon_d

if __name__ == '__main__':
    print "clean dir output...",
    clean_output(dir_output, "amplicon")
    print "OK!"
    amplicon_details = read_bed(path_bed)
    amplicon_data = init_amplicon_data()

    sample_num = 0
    for file in os.listdir(dir_depth_data):
        if re.match('.+\.depth$', file):
            print "processing %s..." % file
            sample_num += 1
            file_name = re.match('(.+)_S\d+_L\d+\.depth', file).group(1)
            with open(os.path.join(dir_depth_data, file), 'rb') as depth_file:
                pass_dict = {}
                for line_depth in depth_file:
                    chr_n = re.match('([^\t]+)\t', line_depth).group(1)
                    pos = int(re.match('[^\t]+\t([^\t]+\t)', line_depth).group(1))
                    depth = int(re.match('(?:[^\t]+\t){2}([^\t\r\n]+)', line_depth).group(1))
                    for key in amplicon_details:
                        if file_name not in amplicon_data[key]["depth"]:
                            amplicon_data[key]["depth"][file_name] = []
                        if key not in pass_dict:
                            pass_dict[key] = 1
                        if chr_n == amplicon_details[key][0] and amplicon_details[key][1] <= pos <= amplicon_details[key][2]:
                            amplicon_data[key]["depth"][file_name].append({"pos": pos, "depth": depth})
                            # print "add %s" % {"pos": pos, "depth": depth}
                            if depth < 10:
                                pass_dict[key] = 0
                            break
                for pass_key in pass_dict:
                    if pass_dict[pass_key] == 0:
                        amplicon_data[pass_key]["failed"] += 1
                    else:
                        amplicon_data[pass_key]["pass"] += 1
    output_amplicon_data(amplicon_data, sample_num, len(amplicon_details))
