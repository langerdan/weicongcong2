#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : create_sample_cover_data
# AUTHOR  : codeunsolved@gmail.com
# CREATED : August 10 2016
# VERSION : v0.0.2
# UPDATE  ：[v0.0.1] September 1 2016
# 1. complete data structure ({data_pinter[sample_cover]=>{sample_data_pointer[frag_cover]=>{frag_data}}};
# 2. add (pass, depth_levels, len_bp, total_reads, mapped_reads, target_reads, 0x_frag) to sdp;
# UPDATE  : [v0.0.2] September 22 2016
# 1. add 100% 0x frag to absent frag;
# 2. use *.stats(samtools stats) to replace *-mismatch.log(countReads)
#    as reads stats(total, mapping, target) data source, target bam comes from `samtools view -b -L $bed`，
#    and discards subprocess.Popen method with open for more compatibility；

from __future__ import division
import os
import re
import sys
import json
import shutil

from base import read_bed
from base import clean_output
from database_connector import MysqlConnector
from config import mysql_config

# CONFIG AREA #
dir_data = sys.argv[1]
path_bed = sys.argv[2]
options = "depth" if len(sys.argv) < 4 else sys.argv[3]

dir_output = os.path.join(r'/Users/codeunsolved/Sites/topgen-dashboard/data', os.path.basename(dir_data))
depth_levels = [0, 20, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 1000]
depth_suffix = "depth"


def output_sample_cover_data(data, sam_num, frag_n):
    dp = {"sample_num": None, "frag_num": None, "sample_cover": data[:]}
    for sample in dp["sample_cover"]:
        dir_sample = os.path.join(os.path.join(dir_output, "sample_cover"), sample["sample_name"])
        if not os.path.exists(dir_sample):
            os.mkdir(dir_sample)
        sdp = sample["sdp"]
        sdp["frag_cover_list"] = []
        for f_key, f_value in frag_details_sorted:
            if f_key in sdp["frag_cover"]:
                with open(os.path.join(dir_sample, "%s.json" % f_key), 'wb') as o_frag:
                    o_frag.write(json.dumps(sdp["frag_cover"][f_key]["frag_data"]))
                sdp["frag_cover_list"].append(sdp["frag_cover"][f_key])
                sdp["frag_cover_list"][-1].pop("frag_data")
        sdp.pop("frag_cover")
        with open(os.path.join(dir_sample, "sample_data_pointer.json"), 'wb') as o_sdp:
            o_sdp.write(json.dumps(sdp))
        sample.pop("sdp")
    dp["sample_num"] = sam_num
    dp["frag_num"] = frag_n
    with open(os.path.join(os.path.join(dir_output, "sample_cover"), "data_pointer.json"), 'wb') as o_dp:
        o_dp.write(json.dumps(dp))


def init_sample_cover(sap_name):
    def init_frag_cover():
        frag_c = {}
        for f_key in frag_details:
            frag_c[f_key] = {"frag_name": f_key,
                             "depth_levels": [],
                             "path": "",
                             "frag_data": {"frag_name": f_key,
                                           "chr_num": re.match('chr(.+)', frag_details[f_key][0]).group(1),
                                           "gene_name": frag_details[f_key][1],
                                           "pos_s": frag_details[f_key][2], "pos_e": frag_details[f_key][3],
                                           "len": frag_details[f_key][3] - frag_details[f_key][2] + 1,
                                           "aver_depth": None, "max_depth": None, "min_depth": None,
                                           "x_labels": [], "depths": []
                                           }
                             }
        return frag_c

    sample_c = {"sample_name": sap_name, "depth_levels": [], "path": "",
                "sdp": {"sample_name": sap_name, "pass": {"0x_percent": 1, "absent_frag": 1, "ALL": 1},
                        "depth_levels": [], "len_bp": None,
                        "total_reads": None, "mapped_reads": None, "target_reads": None,
                        "aver_depth": None, "max_depth": None, "min_depth": None,
                        "0x_frag": {}, "absent_frag": [],
                        "frag_cover": init_frag_cover(),
                        "fastqc": [],
                        "data_ver": "v0.0.2"
                        }
                }
    return sample_c


def init_depth_level_stat():
    dls = {}
    for dl in depth_levels:
        dls[str(dl)] = 0
    return dls


def get_reads_stat(file_n):
    total_reads_num = 0
    mapped_reads_num = 0
    target_reads_num = 0
    with open(os.path.join(dir_data, "%s.stats" % file_n), 'rb') as stats:
        for line_st in stats:
            if re.match('SN\tsequences:\t(\d+)', line_st):
                total_reads_num = int(re.match('SN\tsequences:\t(\d+)', line_st).group(1))
            elif re.match('SN\treads mapped:\t(\d+)', line_st):
                mapped_reads_num = int(re.match('SN\treads mapped:\t(\d+)', line_st).group(1))
                break
    with open(os.path.join(dir_data, "%s.target.stats" % file_n), 'rb') as target_stats:
        for line_st_t in target_stats:
            if re.match('SN\tsequences:\t(\d+)', line_st_t):
                target_reads_num = int(re.match('SN\tsequences:\t(\d+)', line_st_t).group(1))
                break
    return total_reads_num, mapped_reads_num, target_reads_num


def import_qc_seqdata(data):
    m_con = MysqlConnector(mysql_config, 'TopgenNGS')
    insert_g = ("INSERT INTO QC_SeqData "
                "(Project, SAP_id, RUN_bn, SDP, PASS) "
                "VALUES (%s, %s, %s, %s, %s)")
    for d in data:
        if m_con.query("SELECT id FROM QC_SeqData "
                       "WHERE Project=%s AND SAP_id=%s AND RUN_bn=%s",
                       d[:3]).rowcount == 1:
            print "=>record existed! update %s" % d[3:]
            m_con.query("UPDATE QC_SeqData "
                        "SET SDP=%s, PASS=%s "
                        "WHERE Project=%s AND SAP_id=%s AND RUN_bn=%s",
                        (d[3], d[4], d[0], d[1], d[2]))
            m_con.cnx.commit()
        else:
            print "=>insert %s" % d
            m_con.insert(insert_g, d)
    m_con.done()


def cp_fastqc(sap_name, sdp):
    print "copy fastqc html..."
    copy_trigger = 0
    for fqc_html_file in os.listdir(dir_data):
        path_fqc_html_file = os.path.join(dir_data, fqc_html_file)
        if re.search('^%s.+_fastqc\.html' % sap_name, fqc_html_file) and os.path.isfile(path_fqc_html_file):
            if re.search('R1', fqc_html_file):
                print "=>R1's fastqc html: %s..." % fqc_html_file,
                shutil.copy(path_fqc_html_file, os.path.join(dir_output, "fastqc"))
                sdp["fastqc"].append("data/%s/fastqc/%s" % (data_basename, fqc_html_file))
                copy_trigger |= 1
                print "OK! "
            if re.search('R2', fqc_html_file):
                print "=>R2's fastqc html: %s..." % fqc_html_file,
                shutil.copy(path_fqc_html_file, os.path.join(dir_output, "fastqc"))
                sdp["fastqc"].append("data/%s/fastqc/%s" % (data_basename, fqc_html_file))
                copy_trigger |= 2
                print "OK! "
    if ~copy_trigger & 1:
        print "=>R1's fastqc html: nonExistent!"
    if ~copy_trigger & 2:
        print "=>R2's fastqc html: nonExistent!"

if __name__ == '__main__':
    print "clean dir output...",
    clean_output(dir_output, "sample_cover")
    clean_output(dir_output, "fastqc")
    print "OK!"
    frag_details = read_bed(path_bed)
    frag_details_sorted = sorted(frag_details.iteritems(), key=lambda d: (d[1][0], d[1][2]))

    mysql_data = []
    data_basename = os.path.basename(dir_data)
    if re.search('BRCA', data_basename):
        project = 'BRCA'
    elif re.search('onco', data_basename):
        project = '56gene'
    else:
        project = 'unknown'
    run_bn = data_basename
    if re.match('BRCA|onco', run_bn):
        run_bn = re.match('(?:BRCA|onco)(.+)', run_bn).group(1)

    sample_num = 0
    sample_cover = []
    for file in os.listdir(dir_data):
        if re.match('^.+\.%s$' % depth_suffix, file):
            print "processing with %s..." % file
            sample_num += 1
            file_name = re.match('(.+)\.%s' % depth_suffix, file).group(1)
            if re.search('_S\d+', file_name):
                sample_name = re.match('(.+)_S\d+', file_name).group(1)
            elif re.search('autoBox', file_name):
                sample_name = re.match('(.+)_20\d{2}_\d{2}_\d{2}', file_name).group(1)

            with open(os.path.join(dir_data, file), 'rb') as depth_file:
                sample_cover.append(init_sample_cover(sample_name))
                depth_level_stat = {"sample": init_depth_level_stat(), "frag": {}}
                depth_digest_stat = {"sample": {"sum": 0, "len": 0, "max": None, "min": None}, "frag": {}}
                if re.search('depth', options):
                    for line_depth in depth_file:
                        chr_n = re.match('([^\t]+)\t', line_depth).group(1)
                        pos = int(re.match('[^\t]+\t([^\t]+\t)', line_depth).group(1))
                        depth = int(re.match('(?:[^\t]+\t){2}([^\t\r\n]+)', line_depth).group(1))
                        for key, value in frag_details_sorted:
                            # init depth_level_stat["frag"]
                            if key not in depth_level_stat["frag"]:
                                depth_level_stat["frag"][key] = init_depth_level_stat()
                            # init depth_digest_stat["frag"]
                            if key not in depth_digest_stat["frag"]:
                                depth_digest_stat["frag"][key] = {"sum": 0, "len": 0, "max": None, "min": None}

                            if chr_n == value[0] and value[2] <= pos <= value[3]:
                                # count depth_level_stat["sample"] and ["frag"]
                                for depth_level in depth_levels:
                                    if depth_level == 0 and depth > depth_level:
                                        depth_level_stat["sample"][str(depth_level)] += 1
                                        depth_level_stat["frag"][key][str(depth_level)] += 1
                                    elif depth_level != 0 and depth >= depth_level:
                                        depth_level_stat["sample"][str(depth_level)] += 1
                                        depth_level_stat["frag"][key][str(depth_level)] += 1

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

                                # add 0x frag key
                                if depth == 0 and key not in sample_cover[-1]["sdp"]["0x_frag"]:
                                    sample_cover[-1]["sdp"]["0x_frag"][key] = None

                                # add x_labels and depths
                                frag_data = sample_cover[-1]["sdp"]["frag_cover"][key]["frag_data"]
                                if "sample_name" not in frag_data:
                                    frag_data["sample_name"] = sample_name
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
                            for depth_level in depth_levels:
                                frag_cover[key]["depth_levels"].append([str(depth_level), round(
                                    depth_level_stat["frag"][key][str(depth_level)] /
                                    depth_digest_stat["frag"][key]["len"] * 100, 2)])
                            # add frag cover path
                            frag_cover[key]["path"] = "data/%s/sample_cover/%s/%s.json" % \
                                                      (os.path.basename(dir_output), sample_name, key)
                        else:
                            # add absent frag
                            if sample_cover[-1]["sdp"]["pass"]["absent_frag"] == 1:
                                sample_cover[-1]["sdp"]["pass"]["absent_frag"] = 0
                                sample_cover[-1]["sdp"]["pass"]["ALL"] = 0
                            sample_cover[-1]["sdp"]["absent_frag"].append(key)
                            print "[WARNING] %s popped" % key
                    if len(sample_cover[-1]["sdp"]["absent_frag"]) != 0:
                        for p_key in sample_cover[-1]["sdp"]["absent_frag"]:
                            frag_cover.pop(p_key)
                        print "-------popped %d frags-------" % len(sample_cover[-1]["sdp"]["absent_frag"])

                    # add 0x frag 0-percent
                    for key in sample_cover[-1]["sdp"]["0x_frag"]:
                        sample_cover[-1]["sdp"]["0x_frag"][key] = round(
                            (depth_digest_stat["frag"][key]["len"] - depth_level_stat["frag"][key]["0"])
                            / depth_digest_stat["frag"][key]["len"] * 100, 2)
                        if sample_cover[-1]["sdp"]["0x_frag"][key] == 100:
                            # add 100% 0x frag to absent frag
                            if sample_cover[-1]["sdp"]["pass"]["absent_frag"] == 1:
                                sample_cover[-1]["sdp"]["pass"]["absent_frag"] = 0
                                sample_cover[-1]["sdp"]["pass"]["ALL"] = 0
                            sample_cover[-1]["sdp"]["absent_frag"].append(key)
                            print "add 100% 0x frag [{}] to absent frag".format(key)
                    for depth_level in depth_levels:
                        # add sample depth level
                        sample_cover[-1]["depth_levels"].append([str(depth_level), round(
                            depth_level_stat["sample"][str(depth_level)] / depth_digest_stat["sample"]["len"] * 100, 2)])
                        if depth_level == 0 and round(depth_level_stat["sample"][str(depth_level)] / depth_digest_stat["sample"]["len"] * 100, 2) < 99:
                            sample_cover[-1]["sdp"]["pass"]["0x_percent"] = 0
                            sample_cover[-1]["sdp"]["pass"]["ALL"] = 0
                        print "=>depth level: %s, len: %s, sum: %s" % (sample_cover[-1]["depth_levels"][-1],
                                                                       depth_level_stat["sample"][str(depth_level)],
                                                                       depth_digest_stat["sample"]["len"])
                        # add sample_cover path
                        sample_cover[-1]["path"] = "data/%s/sample_cover/%s/sample_data_pointer.json" % \
                                                   (os.path.basename(dir_output), sample_name)

                        # add total length of bp
                        sample_cover[-1]["sdp"]["len_bp"] = depth_digest_stat["sample"]["len"]
                    # add sample depth aver max min
                    sample_cover[-1]["sdp"]["aver_depth"] = round(
                        depth_digest_stat["sample"]["sum"] / depth_digest_stat["sample"]["len"], 2)
                    sample_cover[-1]["sdp"]["max_depth"] = depth_digest_stat["sample"]["max"]
                    sample_cover[-1]["sdp"]["min_depth"] = depth_digest_stat["sample"]["min"]

                    # add sdp sample depth level
                    sample_cover[-1]["sdp"]["depth_levels"] = sample_cover[-1]["depth_levels"]

                    # add reads statistics
                    print "get reads statistics from mismatch..."
                    (sample_cover[-1]["sdp"]["total_reads"],
                     sample_cover[-1]["sdp"]["mapped_reads"],
                     sample_cover[-1]["sdp"]["target_reads"]) = get_reads_stat(file_name)
                    print "=>total_reads: %d, mapped_reads: %d, target_reads: %d" % (
                        sample_cover[-1]["sdp"]["total_reads"],
                        sample_cover[-1]["sdp"]["mapped_reads"],
                        sample_cover[-1]["sdp"]["target_reads"])

                    # add item to QC_SeqData
                    mysql_data.append([project, sample_name, run_bn, sample_cover[-1]["path"],
                                       sample_cover[-1]["sdp"]["pass"]["ALL"]])

                # copy fastqc html
                cp_fastqc(sample_name, sample_cover[-1]["sdp"])

    print "output data...",
    output_sample_cover_data(sample_cover, sample_num, len(frag_details))
    print "OK!"
    print "insert data..."
    import_qc_seqdata(mysql_data)
    # print mysql_data
    print "OK!"
