#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : QC_Reporter
# AUTHOR  : codeunsolved@gmail.com
# CREATED : August 10 2016
# VERSION : v0.0.3
# UPDATE  ：[v0.0.1] September 1 2016
# 1. complete data structure ({data_pinter[sample_cover]=>{sample_data_pointer[frag_cover]=>{frag_data}}};
# 2. add (pass, depth_levels, len_bp, total_reads, mapped_reads, target_reads, 0x_frag) to sdp;
# UPDATE  : [v0.0.2] September 22 2016
# 1. add 100% 0x frag to absent frag;
# 2. use *.stats(samtools stats) to replace *-mismatch.log(countReads)
#    as reads stats(total, mapping, target) data source, target bam comes from `samtools view -b -L $bed`，
#    and discards subprocess.Popen method with open for more compatibility；
# UPDATE  : [v0.0.3] November 22 2016
# 1. add module pysam to parse bam file;
# 2. add Coverage Uniformity statistic(Refer: https://github.com/eulaf/CFseq/blob/master/pipeline/qc/uniformity_coverage.py);
# 3. add Reads statistic via pysam(including each region); 
# 4. adjust Project, SAP_id, RUN_bn handle and program structure;
# 5. add bed_filename to sdp;
# 6. change name from 'create_sample_cover_data' to 'QC_Reporter'(may add option: output report);

from __future__ import division
import os
import re
import sys
import json
import shutil
import argparse

import pysam

from base import read_bed
from base import clean_output
from base import print_colors
from base import handle_sap_id
from config import mysql_config
from database_connector import MysqlConnector

# CONFIG AREA #
__VERSION__ = 'v0.0.3'
depth_levels = [0, 20, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 1000]


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
                                           "mean_depth": None, "max_depth": None, "min_depth": None,
                                           "x_labels": [], "depths": []
                                           }
                             }
        return frag_c

    def init_frag_reads():
        frag_r = {}
        for f_key in frag_details:
            frag_r[f_key] = None
        return frag_r

    sample_c = {"sample_name": sap_name, "depth_levels": [], "path": "",
                "sdp": {"sample_name": sap_name, "bed_filename": bed_filename,
                        "pass": {"0x_percent": None, "absent_frag": 0, "coverage_unifor": None, "min_reads": None, "OVERALL": None},
                        "depth_levels": [], "len_bp": None,
                        "total_reads": None, "mapped_reads": None, "target_reads": None,
                        "total_reads_pysam": None, "mapped_reads_pysam": None, "target_reads_pysam": 0,
                        "mean_reads": None, "max_reads": None, "min_reads": None,
                        "frag_reads": init_frag_reads(),
                        "mean_0_2x": None, "uniformity_0_2x": None,
                        "mean_0_5x": None, "uniformity_0_5x": None,
                        "mean_depth": None, "max_depth": None, "min_depth": None,
                        "0x_frag": {}, "absent_frag": [],
                        "frag_cover": init_frag_cover(),
                        "fastqc": [],
                        "data_ver": __VERSION__
                        }
                }
    return sample_c


def init_depth_level_stat():
    dls = {}
    for dl in depth_levels:
        dls[str(dl)] = 0
    return dls


def get_reads_stats(file_n):
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


def pysam_stat(path_bam, sdp):
    def stat_mean(l):
        sum = 0
        for x in l:
            sum += x
        return sum / len(l)

    samfile = pysam.AlignmentFile(path_bam, "rb")
    # Reads statistics
    sdp["mapped_reads_pysam"] = samfile.mapped
    sdp["total_reads_pysam"] = samfile.unmapped + sdp["mapped_reads_pysam"]
    for f_key in frag_details:
        sdp["frag_reads"][f_key] = samfile.count(frag_details[f_key][0], frag_details[f_key][2], frag_details[f_key][3])
        sdp["target_reads_pysam"] += sdp["frag_reads"][f_key]

    # Coverage Uniformity
    reads = sdp["frag_reads"].values()
    sdp["max_reads"] = max(reads)
    sdp["min_reads"] = min(reads)
    sdp["mean_reads"] = round(stat_mean(reads), 2)

    sdp["mean_0_2x"] = sdp["mean_reads"] * 0.2
    sdp["uniformity_0_2x"] = round(len([x for x in reads if x > sdp["mean_0_2x"]]) / len(reads) * 100, 2) if reads else 0
    sdp["mean_0_5x"] = sdp["mean_reads"] * 0.5
    sdp["uniformity_0_5x"] = round(len([x for x in reads if x > sdp["mean_0_5x"]]) / len(reads) * 100, 2) if reads else 0

    sdp["pass"]["min_reads"] = sdp["min_reads"]
    sdp["pass"]["coverage_unifor"] = sdp["uniformity_0_2x"]


def cp_fastqc(sap_name, sdp):
    copy_trigger = 0
    for fqc_html_file in os.listdir(dir_data):
        if re.search('^%s.+_fastqc\.html' % sap_name, fqc_html_file):
            path_fqc_html_file = os.path.join(dir_data, fqc_html_file)
            if re.search('R1', fqc_html_file):
                print print_colors("=>R1's fastqc html: %s ..." % fqc_html_file),
                shutil.copy(path_fqc_html_file, os.path.join(dir_output, "fastqc"))
                sdp["fastqc"].append("data/%s/fastqc/%s" % (dir_name, fqc_html_file))
                copy_trigger |= 1
                print print_colors("OK!", 'green')
            if re.search('R2', fqc_html_file):
                print print_colors("=>R2's fastqc html: %s ..." % fqc_html_file),
                shutil.copy(path_fqc_html_file, os.path.join(dir_output, "fastqc"))
                sdp["fastqc"].append("data/%s/fastqc/%s" % (dir_name, fqc_html_file))
                copy_trigger |= 2
                print print_colors("OK!", 'green')
    if ~copy_trigger & 1:
        print print_colors("  R1's fastqc html: nonExistent!", 'red')
    if ~copy_trigger & 2:
        print print_colors("  R2's fastqc html: nonExistent!", 'red')


def pass_check(sdp):
    for key in sdp["pass"]:
        if key == "0x_percent":
            if sdp["pass"][key] > 1:
                sdp["pass"]["OVERALL"] = 0
                return
        elif key == "absent_frag":
            if sdp["pass"][key]:
                sdp["pass"]["OVERALL"] = 0
                return
        elif key == "coverage_unifor":
            if sdp["pass"][key] < 98:
                sdp["pass"]["OVERALL"] = 0
                return
        elif key == "min_reads":
            if sdp["pass"][key] < 80:
                sdp["pass"]["OVERALL"] = 0
                return
    sdp["pass"]["OVERALL"] = 1


def import_lab(data):
    table = "%s_lab" % project
    insert_g = ("INSERT INTO {0} "
                "(`SAP_id`, `RUN_bn`) "
                "VALUES (%s, %s)".format(table))
    update = 0
    insert = 0
    ignore = 0
    for sap_id in data:
        item = '%s,,,0000-00-00,,,,,0000-00-00,,,,,,,,,,,,,0000-00-00,%s,,,,,,INIT' % (sap_id, run_bn)
        item = item.split(',')
        if m_con.query("SELECT id FROM {0} "
                       "WHERE SAP_id=%s AND RUN_bn=%s".format(table),
                       (item[0], item[22])).rowcount == 1:
            ignore += 1
        else:
            insert += 1
            m_con.insert(insert_g, (item[0], item[22]))
    print print_colors("insert %s" % insert if insert else "" + 
                       "update %s" % update if update else "" +
                       "ignore %s" % ignore if ignore else "", 'grey'),


def import_qc_seqdata(data):
    insert_g = ("INSERT INTO QC_SeqData "
                "(Project, SAP_id, RUN_bn, SDP, PASS) "
                "VALUES (%s, %s, %s, %s, %s)")
    update = 0
    insert = 0
    ignore = 0
    for d in data:
        if m_con.query("SELECT id FROM QC_SeqData "
                       "WHERE Project=%s AND SAP_id=%s AND RUN_bn=%s",
                       d[:3]).rowcount == 1:
            if args.update:
                update += 1
                m_con.query("UPDATE QC_SeqData "
                            "SET SDP=%s, PASS=%s "
                            "WHERE Project=%s AND SAP_id=%s AND RUN_bn=%s",
                            (d[3], d[4], d[0], d[1], d[2]))
                m_con.cnx.commit()
            else:
                ignore += 1
        else:
            insert += 1
            m_con.insert(insert_g, d)
    print print_colors("insert %s" % insert if insert else "" + 
                       "update %s" % update if update else "" +
                       "ignore %s" % ignore if ignore else "", 'grey'),


def main():
    sample_num = 0
    sample_cover = []
    sample_names = []
    mysql_qc = []
    for f in os.listdir(dir_data):
        if re.match('^.+\.depth$', f):
            print print_colors("<%s>" % f, 'red')
            sample_num += 1

            # handle sample name
            file_name = re.match('(.+)\.depth$', f).group(1)
            sample_name = handle_sap_id(file_name)

            # append data to sample_names
            sample_names.append(sample_name)

            # init data structure
            sample_cover.append(init_sample_cover(sample_name))

            if args.skip_depth:
                depth_level_stat = {"sample": init_depth_level_stat(), "frag": {}}
                depth_digest_stat = {"sample": {"sum": 0, "len": 0, "max": None, "min": None}, "frag": {}}
                sample_data_pointer = sample_cover[-1]["sdp"]
                with open(os.path.join(dir_data, f), 'rb') as depth_file:
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
                                if depth == 0 and key not in sample_data_pointer["0x_frag"]:
                                    sample_data_pointer["0x_frag"][key] = None

                                # add x_labels and depths
                                frag_data = sample_data_pointer["frag_cover"][key]["frag_data"]
                                if "sample_name" not in frag_data:
                                    frag_data["sample_name"] = sample_name
                                frag_data["x_labels"].append(pos)
                                frag_data["depths"].append(depth)
                                break

                    frag_cover = sample_data_pointer["frag_cover"]
                    for key in frag_cover:
                        if len(frag_cover[key]["frag_data"]["x_labels"]) != 0:
                            # get frag len and sample len
                            depth_digest_stat["sample"]["len"] += len(frag_cover[key]["frag_data"]["x_labels"])
                            depth_digest_stat["frag"][key]["len"] = len(frag_cover[key]["frag_data"]["x_labels"])
                            # add frag depth(mean max min)
                            frag_cover[key]["frag_data"]["mean_depth"] = round(
                                depth_digest_stat["frag"][key]["sum"] / depth_digest_stat["frag"][key]["len"], 2)
                            frag_cover[key]["frag_data"]["max_depth"] = depth_digest_stat["frag"][key]["max"]
                            frag_cover[key]["frag_data"]["min_depth"] = depth_digest_stat["frag"][key]["min"]
                            # add frag depth level
                            for depth_level in depth_levels:
                                frag_cover[key]["depth_levels"].append(
                                    [str(depth_level), round(
                                        depth_level_stat["frag"][key][str(depth_level)] /
                                        depth_digest_stat["frag"][key]["len"] * 100, 2
                                    )]
                                )
                            # add frag cover path
                            frag_cover[key]["path"] = "data/%s/sample_cover/%s/%s.json" % \
                                                      (os.path.basename(dir_output), sample_name, key)
                        else:
                            # add absent frag
                            if sample_data_pointer["pass"]["absent_frag"] is None:
                                sample_data_pointer["pass"]["absent_frag"] = 1
                            else:
                                sample_data_pointer["pass"]["absent_frag"] += 1
                            sample_data_pointer["absent_frag"].append(key)
                            print print_colors("[WARNING] %s popped" % key, 'yellow')
                    if len(sample_data_pointer["absent_frag"]) != 0:
                        for p_key in sample_data_pointer["absent_frag"]:
                            frag_cover.pop(p_key)
                        print print_colors("------- popped %d frags -------" % len(sample_data_pointer["absent_frag"]), 'red')

                    # add 0x frag 0-percent
                    for key in sample_data_pointer["0x_frag"]:
                        sample_data_pointer["0x_frag"][key] = round(
                            (depth_digest_stat["frag"][key]["len"] - depth_level_stat["frag"][key]["0"])
                            / depth_digest_stat["frag"][key]["len"] * 100, 2)
                        if sample_data_pointer["0x_frag"][key] == 100:
                            # add 100% 0x frag to absent frag
                            if sample_data_pointer["pass"]["absent_frag"] is None:
                                sample_data_pointer["pass"]["absent_frag"] = 1
                            else:
                                sample_data_pointer["pass"]["absent_frag"] += 1
                            sample_data_pointer["absent_frag"].append(key)
                            print print_colors("add 100% 0x frag [{}] to absent frag".format(key), 'yellow')
                    for depth_level in depth_levels:
                        # add sample depth level
                        depth_level_percent = round(depth_level_stat["sample"][str(depth_level)] / depth_digest_stat["sample"]["len"] * 100, 2)
                        sample_cover[-1]["depth_levels"].append([str(depth_level), depth_level_percent])
                        if depth_level == 0:
                            sample_data_pointer["pass"]["0x_percent"] = round(100 - depth_level_percent, 2)
                        print print_colors("=>depth level: %s, len: %s, sum: %s" % (
                                           sample_cover[-1]["depth_levels"][-1],
                                           depth_level_stat["sample"][str(depth_level)],
                                           depth_digest_stat["sample"]["len"]), 'green')
                        # add sample_cover path
                        sample_cover[-1]["path"] = "data/%s/sample_cover/%s/sample_data_pointer.json" % \
                                                   (os.path.basename(dir_output), sample_name)

                        # add total length of bp
                        sample_data_pointer["len_bp"] = depth_digest_stat["sample"]["len"]
                    # add sample depth(mean max min)
                    sample_data_pointer["mean_depth"] = round(
                        depth_digest_stat["sample"]["sum"] / depth_digest_stat["sample"]["len"], 2)
                    sample_data_pointer["max_depth"] = depth_digest_stat["sample"]["max"]
                    sample_data_pointer["min_depth"] = depth_digest_stat["sample"]["min"]

                    # add sdp sample depth level
                    sample_data_pointer["depth_levels"] = sample_cover[-1]["depth_levels"]

            # Reads statistics via samtools stats
            print print_colors("• get Reads statistics from .stats ...")
            (sample_data_pointer["total_reads"],
             sample_data_pointer["mapped_reads"],
             sample_data_pointer["target_reads"]) = get_reads_stats(file_name)
            print print_colors("=>total_reads: %d, mapped_reads: %d, target_reads: %d" % (
                               sample_data_pointer["total_reads"],
                               sample_data_pointer["mapped_reads"],
                               sample_data_pointer["target_reads"]), 'green')

            # Reads statistics via pysam (including each region)
            # Coverage Uniformity statistics
            print print_colors("• get Reads statistics and get Coverage Unniformoty from .bam ...")
            pysam_stat(os.path.join(dir_data, "%s.bam" % file_name), sample_data_pointer)
            print print_colors("=>total_reads: %d, mapped_reads: %d, target_reads: %d" % (
                               sample_data_pointer["total_reads_pysam"],
                               sample_data_pointer["mapped_reads_pysam"],
                               sample_data_pointer["target_reads_pysam"],), 'green')
            print print_colors("=>max reads: %d, min reads: %d, mean reads: %d" % (
                               sample_data_pointer["max_reads"],
                               sample_data_pointer["min_reads"],
                               sample_data_pointer["mean_reads"]), 'green')
            print print_colors("=>Coverage Uniformity >0.2x: %f, >0.5x: %f" % (
                               sample_data_pointer["uniformity_0_2x"],
                               sample_data_pointer["uniformity_0_5x"]), 'green')

            # pass check
            pass_check(sample_data_pointer)

            # append data to mysql_qc
            mysql_qc.append([project, sample_name, run_bn, sample_cover[-1]["path"],
                               sample_data_pointer["pass"]["OVERALL"]])

            # copy FASTQC html
            print print_colors("• copy fastqc html ...")
            cp_fastqc(sample_name, sample_data_pointer)

    print print_colors("• output data ..."),
    output_sample_cover_data(sample_cover, sample_num, len(frag_details))
    print print_colors("OK!", 'green')

    print print_colors("• import data to Lab ..."),
    import_lab(sample_names)
    print print_colors("OK!", 'green')
    print print_colors("• import data to QC_SeqData ..."),
    import_qc_seqdata(mysql_qc)
    print print_colors("OK!", 'green')

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='create QC data for Topgen-Dashboard and reporter')
    parser.add_argument('dir_data', type=str, help="Specify path of data's directory")
    parser.add_argument('path_bed', type=str, help="Specify path of bed file")
    parser.add_argument('-p', '--project', type=str, help="Specify Project")
    parser.add_argument('-r', '--run_bn', type=str, help="Specify RUN batch No.")
    parser.add_argument('-kd', '--skip_depth', action='store_false', help="skip depth statistics")
    parser.add_argument('-u', '--update', action='store_true', help='update import data')

    args = parser.parse_args()
    
    dir_data = args.dir_data
    path_bed = args.path_bed
    dir_output = os.path.join('/Users/codeunsolved/Sites/topgen-dashboard/data', os.path.basename(dir_data))

    print print_colors("• clean dir output ..."),
    clean_output(dir_output, "sample_cover")
    clean_output(dir_output, "fastqc")
    print print_colors("OK!", 'green')

    dir_name = os.path.basename(dir_data)

    # handle project
    if args.project is not None:
        project = args.project
    else:
        if re.search('BRCA', dir_name):
            project = 'BRCA'
        elif re.search('42gene', dir_name):
            project = '42gene'
        elif re.search('56gene', dir_name):
            project = '56gene'
        else:
            raise Exception("Unknown project for %s" % dir_name)

    # handle run batch number
    if args.run_bn is not None:
        run_bn = args.run_bn
    else:
        if re.match('BRCA|onco', dir_name):
            run_bn = re.match('(?:BRCA|onco)(\d+)', dir_name).group(1)
        else:
            raise Exception("Unknown RUN batch No. for %s" % dir_name)

    print print_colors("Project : ", 'yellow') + print_colors(project, 'green') + print_colors(" RUN bn: ", 'yellow') + print_colors(run_bn, 'green')

    bed_filename = os.path.basename(args.path_bed)
    frag_details = read_bed(path_bed)
    frag_details_sorted = sorted(frag_details.iteritems(), key=lambda d: (d[1][0], d[1][2]))

    m_con = MysqlConnector(mysql_config, 'TopgenNGS')
    main()
    m_con.done()
