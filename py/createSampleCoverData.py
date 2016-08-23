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
path_bed = r'/Users/codeunsolved/Downloads/NGS-Data/bed/BRAC-1606-3.bed'
dir_depth_data = r'/Users/codeunsolved/Downloads/NGS-Data/BRAC160727-3'
dir_output = r'/Users/codeunsolved/Sites/topgen-dashboard/data/BRAC160727'
depth_level = [0, 20, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 1000]
depth_ext = "depth"


def output_sample_cover_data(data, sample_n, frag_n):
    dp = {"sample_num": None, "frag_num": None, "sample_cover": data[:]}
    for each_sample in dp["sample_cover"]:
        sample_name = each_sample["sample_name"]
        dir_sample = os.path.join(os.path.join(dir_output, "sample_cover"), sample_name)
        if not os.path.exists(dir_sample):
            os.mkdir(dir_sample)
        sdp = each_sample["sdp"]
        sdp["frag_cover_list"] = []
        for f_key, f_value in frag_details_sorted:
            if f_key in sdp["frag_cover"]:
                with open(os.path.join(dir_sample, "%s.json" % f_key), 'wb') as w_obj_f:
                    w_obj_f.write(json.dumps(sdp["frag_cover"][f_key]["frag_data"]))
                sdp["frag_cover_list"].append(sdp["frag_cover"][f_key])
                sdp["frag_cover_list"][-1]["path"] = \
                    "data/%s/sample_cover/%s/%s.json" % (os.path.basename(dir_output), sample_name, f_key)
                sdp["frag_cover_list"][-1].pop("frag_data")
        sdp.pop("frag_cover")
        with open(os.path.join(dir_sample, "sample_data_pointer.json"), 'wb') as w_obj_s:
            w_obj_s.write(json.dumps(sdp))
        each_sample["path"] = "data/%s/sample_cover/%s/sample_data_pointer.json" % (os.path.basename(dir_output), sample_name)
        each_sample.pop("sdp")
    dp["sample_num"] = sample_n
    dp["frag_num"] = frag_n
    with open(os.path.join(os.path.join(dir_output, "sample_cover"), "data_pointer.json"), 'wb') as w_obj_d:
        w_obj_d.write(json.dumps(dp))


def init_sample_cover(sample_name):
    def init_frag_cover():
        frag_c = {}
        for f_key in frag_details:
            frag_c[f_key] = {"frag_name": f_key,
                             "depth_level": [],
                             "path": "",
                             "frag_data": {"frag_name": f_key,
                                           "chr_num": re.match('chr(.+)', frag_details[f_key][0]).group(1),
                                           "pos_s": frag_details[f_key][1], "pos_e": frag_details[f_key][2],
                                           "gene_name": frag_details[f_key][3],
                                           "len": frag_details[f_key][2] - frag_details[f_key][1] + 1,
                                           "aver_depth": None, "max_depth": None, "min_depth": None,
                                           "x_labels": [], "depths": []}}
        return frag_c

    sample_c = {"sample_name": sample_name, "depth_level": [], "path": "",
                "sdp": {"sample_name": sample_name, "depth_level": [],
                        "aver_depth": None, "max_depth": None, "min_depth": None, "frag_cover": init_frag_cover(),
                        "absent_frag": []}}
    return sample_c


def init_depth_level_stat():
    dls = {}
    for each_dl in depth_level:
        dls[str(each_dl)] = 0
    return dls


print "clean dir output...",
clean_output(dir_output, "sample_cover")
print "OK!"
frag_details = read_bed(path_bed)
frag_details_sorted = sorted(frag_details.iteritems(), key=lambda d: (d[1][0], d[1][1]))

sample_num = 0
sample_cover = []
for each_file in os.listdir(dir_depth_data):
    if re.match('^.+\.%s$' % depth_ext, each_file):
        print "processing with %s..." % each_file
        sample_num += 1
        file_name = re.match('(.+)_S\d+_L\d+\.%s' % depth_ext, each_file).group(1)
        with open(os.path.join(dir_depth_data, each_file), 'rb') as r_obj:
            sample_cover.append(init_sample_cover(file_name))
            depth_level_stat = {"sample": init_depth_level_stat(), "frag": {}}
            depth_digest_stat = {"sample": {"sum": 0, "len": 0, "max": None, "min": None}, "frag": {}}
            for line_depth in r_obj:
                chr_n = re.match('([^\t]+)\t', line_depth).group(1)
                pos = int(re.match('[^\t]+\t([^\t]+\t)', line_depth).group(1))
                depth = int(re.match('(?:[^\t]+\t){2}([^\t\n\r]+)', line_depth).group(1))
                for key, value in frag_details_sorted:
                    # init depth_level_stat["frag"]
                    if key not in depth_level_stat["frag"]:
                        depth_level_stat["frag"][key] = init_depth_level_stat()
                    # init depth_digest_stat["frag"]
                    if key not in depth_digest_stat["frag"]:
                        depth_digest_stat["frag"][key] = {"sum": 0, "len": 0, "max": None, "min": None}

                    if chr_n == value[0] and value[1] <= pos <= value[2]:
                        # count depth_level_stat["sample"] and ["frag"]
                        for each_depth_level in depth_level:
                            if each_depth_level == 0 and depth > each_depth_level:
                                depth_level_stat["sample"][str(each_depth_level)] += 1
                                depth_level_stat["frag"][key][str(each_depth_level)] += 1
                            elif each_depth_level != 0 and depth >= each_depth_level:
                                depth_level_stat["sample"][str(each_depth_level)] += 1
                                depth_level_stat["frag"][key][str(each_depth_level)] += 1

                        # count depth_digest_stat sum
                        depth_digest_stat["sample"]["sum"] += depth
                        depth_digest_stat["frag"][key]["sum"] += depth
                        # count depth_digest_stat max
                        if depth > depth_digest_stat["sample"]["max"] or depth_digest_stat["sample"]["max"] is None:
                            depth_digest_stat["sample"]["max"] = depth
                        if depth > depth_digest_stat["frag"][key]["max"] or depth_digest_stat["frag"][key]["max"] is None:
                            depth_digest_stat["frag"][key]["max"] = depth
                        # count depth_digest_stat min
                        if depth < depth_digest_stat["sample"]["min"] or depth_digest_stat["sample"]["min"] is None:
                            depth_digest_stat["sample"]["min"] = depth
                        if depth < depth_digest_stat["frag"][key]["min"] or depth_digest_stat["frag"][key]["min"] is None:
                            depth_digest_stat["frag"][key]["min"] = depth

                        # add x_labels and depths
                        frag_data = sample_cover[-1]["sdp"]["frag_cover"][key]["frag_data"]
                        if "sample_name" not in frag_data:
                            frag_data["sample_name"] = file_name
                        frag_data["x_labels"].append(pos)
                        frag_data["depths"].append(depth)
                        break
            frag_cover = sample_cover[-1]["sdp"]["frag_cover"]
            for key in frag_cover:
                if len(frag_cover[key]["frag_data"]["x_labels"]) != 0:
                    # get frag len and sample len
                    depth_digest_stat["sample"]["len"] += len(frag_cover[key]["frag_data"]["x_labels"])
                    depth_digest_stat["frag"][key]["len"] = len(frag_cover[key]["frag_data"]["x_labels"])
                    # add frag depth aver max min
                    frag_cover[key]["frag_data"]["aver_depth"] = round(
                        depth_digest_stat["frag"][key]["sum"] / depth_digest_stat["frag"][key]["len"], 2)
                    frag_cover[key]["frag_data"]["max_depth"] = depth_digest_stat["frag"][key]["max"]
                    frag_cover[key]["frag_data"]["min_depth"] = depth_digest_stat["frag"][key]["min"]
                    # add frag depth level
                    for each_depth_level in depth_level:
                        frag_cover[key]["depth_level"].append([str(each_depth_level), round(
                            depth_level_stat["frag"][key][str(each_depth_level)] /
                            depth_digest_stat["frag"][key]["len"] * 100, 2)])
                else:
                    sample_cover[-1]["sdp"]["absent_frag"].append(key)
                    print "[WARNING] %s popped" % key
            if len(sample_cover[-1]["sdp"]["absent_frag"]) != 0:
                for p_key in sample_cover[-1]["sdp"]["absent_frag"]:
                    frag_cover.pop(p_key)
                print "-------popped %d frags-------" % len(sample_cover[-1]["sdp"]["absent_frag"])
            for each_depth_level in depth_level:
                # add sample depth level
                sample_cover[-1]["depth_level"].append([str(each_depth_level), round(
                    depth_level_stat["sample"][str(each_depth_level)] / depth_digest_stat["sample"]["len"] * 100, 2)])
                print "=>depth level: %s, len: %s, sum: %s" % (sample_cover[-1]["depth_level"][-1],
                                                               depth_level_stat["sample"][str(each_depth_level)],
                                                               depth_digest_stat["sample"]["len"])
            # add sample depth aver max min
            sample_cover[-1]["sdp"]["aver_depth"] = round(
                depth_digest_stat["sample"]["sum"] / depth_digest_stat["sample"]["len"], 2)
            sample_cover[-1]["sdp"]["max_depth"] = depth_digest_stat["sample"]["max"]
            sample_cover[-1]["sdp"]["min_depth"] = depth_digest_stat["sample"]["min"]

            # add sdp sample depth level
            sample_cover[-1]["sdp"]["depth_level"] = sample_cover[-1]["depth_level"]
print "output data...",
output_sample_cover_data(sample_cover, sample_num, len(frag_details))
print "OK!"
