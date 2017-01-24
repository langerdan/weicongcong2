#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : compare
# AUTHOR  : codeunsolved@gmail.com
# CREATED : January 11 2017
# VERSION : v0.0.1
# UPDATE  : [v0.0.1] January 23 2017
# 1. add compare VCF;
# 2. add compare BED;

import os
import re
import random
import argparse
from argparse import RawTextHelpFormatter

import xlrd

from lib.base import read_bed
from lib.base import parse_vcf
from lib.base import print_colors


def compare_vcf():
    def get_v_full(l, v_chr_pos):
        for x in l:
            if re.match('%s-' % v_chr_pos, x):
                return x
        raise Exception('No variant calling full in %s' % v_chr_pos)

    def parse_cross_xls(p_xls):
        vcf_main = []
        try:
            report = xlrd.open_workbook(p_xls)
        except Exception, e:
            print ":", e
        else:
            sample_id = re.match('(.+)_SNP\.xls', os.path.basename(p_xls)).group(1)

            table = report.sheet_by_name(sample_id)
            nrows = table.nrows
            ncols = table.ncols
            for i in range(1, nrows):
                chr_n = table.cell(i, 0).value
                pos = int(table.cell(i, 1).value)
                ref = table.cell(i, 3).value
                alt = table.cell(i, 4).value
                vcf_main.append([chr_n, pos, ref, alt])
            return vcf_main

    def parse_ts_xls(p_xls):
        vcf_main = []
        with open(p_xls, 'rb') as ts_xls:
            for i, line in enumerate(ts_xls):
                if i == 0:
                    continue
                line_cont = line.split('\t')

                # filter Allele Call in [Absnet, NO CALL]
                if line_cont[4] in ['Absent', 'No Call']:
                    continue

                chr_n = line_cont[0]
                pos = int(line_cont[1])
                ref = line_cont[2]
                alt = line_cont[3]
                vcf_main.append([chr_n, pos, ref, alt])
        return vcf_main

    def output_v(s, d, n_a, n_b):
        with open(os.path.join(args.dir_output, "compare_report-%s-%s" % (n_a, n_b)), 'wb') as o:
            for line in s:
                o.write("%s\n" % "\t".join([str(x) for x in line]))
            o.write('---\t---\t---\n')
            for line in d:
                o.write("%s\n" % "\t".join([str(x) for x in line]))

    sap_a = args.sample_a
    sap_b = args.sample_b
    name_a = os.path.basename(sap_a)
    name_b = os.path.basename(sap_b)

    summary = [["A = %s" % name_a, "->", "B = %s" % name_b], ["Append", "Miss", "Inconsistent", "Match"]]
    append_details = [["Status", "Details"]]
    details = []

    append = 0
    miss = 0
    inconsistent = 0
    match = 0

    v_sap_a = []
    v_sap_b = []

    print print_colors("<%s -> %s>" % (sap_a, sap_b))

    # Sample A
    print print_colors(" - %s ..." % name_a),
    if args.cross_xls:
        vcf_content_a = parse_cross_xls(sap_a)
    else:
        vcf_content_a = parse_vcf(sap_a)
    for v in vcf_content_a:
        if args.cross_xls:
            v_sap_a.append('-'.join([str(x) for x in v[:4]]))
        else:
            v_sap_a.append('-'.join([str(x) for x in v[:2] + v[3:5]]))
        v_sap_a.append('-'.join([str(x) for x in v[:2]]))
    print print_colors(str(len(v_sap_a)/2), 'green')

    # Sample B
    print print_colors(" - %s ..." % name_b),
    if args.ts_xls:
        vcf_content_b = parse_ts_xls(sap_b)
    else:
        vcf_content_b = parse_vcf(sap_b)
    for v in vcf_content_b:
        if args.ts_xls:
            v_full = '-'.join([str(x) for x in v[:4]])
        else:
            v_full = '-'.join([str(x) for x in v[:2] + v[3:5]])
        v_chr_pos = '-'.join([str(x) for x in v[:2]])
        v_sap_b.append(v_full)
        v_sap_b.append(v_chr_pos)

        if v_full not in v_sap_a and v_chr_pos in v_sap_a:
            inconsistent += 1
            details.append(["Inconsistent", "A: %s" % get_v_full(v_sap_a, v_chr_pos), "B: %s" % v_full])
        elif v_chr_pos not in v_sap_a:
            miss += 1
            details.append(["Miss", "B: %s" % v_full])
        elif v_full in v_sap_a:
            match += 1
            details.append(["Match", v_full])
        else:
            raise Exception("Unexpected case with [%s]" % v_full)
    print print_colors(str(len(v_sap_b)/2), 'green')

    for v_header in v_sap_a:
        if re.match('chr[1-9XYM]+-\d+-[^\-]+-[^\-]+', v_header):
            v_chr_pos = re.match('(chr[1-9XYM]+-\d+)', v_header).group(1)
            if v_chr_pos not in v_sap_b:
                append += 1
                append_details.append(["Append", "A: %s" % v_header])
    print print_colors("Append %d, Miss %d, Inconsistent %d, Match %d" % (append, miss, inconsistent, match), 'green')
    summary.append([append, miss, inconsistent, match])
    output_v(summary, append_details + details, name_a, name_b)

    def filter_non_overlap(p_bed, d_n, name_n):
        left = []

        print "-------"
        print print_colors("%s Filter: %s" % (name_n, os.path.basename(p_bed)))
        bed_n = read_bed(p_bed, 'list')
        for n in d_n:
            match_trigger = 0

            v = re.match('[AB]: (.+)$', n[1]).group(1).split('-')
            chr_n = v[0]
            pos = int(v[1])
            for f in bed_n:
                if f["chr"] == chr_n and f["start"] <= pos <= f["end"]:
                    match_trigger = 1
                    break
                else:
                    continue
            if not match_trigger:
                left.append('-'.join(v))

        print print_colors("%s after filter: %s" % (name_n, len(left)), 'red')
        print ', '.join(left)

    if args.append_bed:
        filter_non_overlap(args.append_bed, append_details[1:], "Append")
    if args.miss_bed:
        miss_details = [x for x in details if x[0] == 'Miss']
        filter_non_overlap(args.miss_bed, miss_details, "Miss")


def compare_bed():
    def merge(l):
        merge_l = []
        merged_i = []
        for i, raw in enumerate(l):
            if i in merged_i:
                continue
            merged_i.append(i)
            for j, f in enumerate(l):
                if j in merged_i:
                    continue
                if raw["chr"] == f["chr"]:
                    if f["start"] >= raw["end"] or raw["start"] >= f["end"]:
                        continue
                    elif f["start"] > raw["start"] and raw["end"] > f["start"] and f["end"] > raw["end"]:
                        raw["end"] = f["end"]
                        merged_i.append(j)
                    elif raw["start"] > f["start"] and f["end"] > raw["start"] and raw["end"] > f["end"]:
                        raw["start"] = f["start"]
                        merged_i.append(j)
                    elif raw["start"] <= f["start"] and raw["end"] >= f["end"]:
                        merged_i.append(j)
                    elif f["start"] <= raw["start"] and f["end"] >= raw["end"]:
                        raw["start"] = f["start"]
                        raw["end"] = f["end"]
                        merged_i.append(j)
                    else:
                        raise Exception("[MERGE]Unexcepted RAW F range: %s RAW[%s - %s] F[%s - %s]" % (raw["chr"], raw["start"], raw["end"], f["start"], f["end"]))
                else:
                    continue
            merge_l.append(raw)
        return merge_l

    def get_a_left(a_l, b):
        a_l_left = []
        for a in a_l:
            if a["chr"] == b["chr"]:
                if b["start"] >= a["end"] or a["start"] >= b["end"]:
                    a_l_left.append(a.copy())
                elif b["start"] > a["start"] and a["end"] > b["start"] and b["end"] >= a["end"]:
                    a_l_left.append(a.copy())
                    a_l_left[-1]["end"] = b["start"]
                    a_l_left[-1]["gene"] = "[%s<%s]" % (a_l_left[-1]["gene"], b["gene"])
                elif a["start"] >= b["start"] and b["end"] > a["start"] and a["end"] > b["end"]:
                    a_l_left.append(a.copy())
                    a_l_left[-1]["start"] = b["end"]
                    a_l_left[-1]["gene"] = "[%s>%s]" % (b["gene"], a_l_left[-1]["gene"])
                elif a["start"] < b["start"] and a["end"] > b["end"]:
                    a_l_left.append(a.copy())
                    a_l_left[-1]["end"] = b["start"]
                    a_l_left[-1]["gene"] = "[%s<%s]" % (a_l_left[-1]["gene"], b["gene"])
                    a_l_left.append(a.copy())
                    a_l_left[-1]["start"] = b["end"]
                    a_l_left[-1]["gene"] = "[%s>%s]" % (b["gene"], a_l_left[-1]["gene"])
                elif b["start"] <= a["start"] and b["end"] >= a["end"]:
                    pass
                else:
                    raise Exception("[LEFT]Unexcepted A B range: %s A[%s - %s] B[%s - %s]" % (a["chr"], a["start"], a["end"], b["start"], b["end"]))
            else:
                a_l_left.append(a.copy())
        return a_l_left

    def get_ab_overlap(a, b):
        if a["chr"] == b["chr"]:
            if b["start"] >= a["end"] or a["start"] >= b["end"]:
                if "match" not in a:
                    a["match"] = 0
                return a
            elif b["start"] > a["start"] and a["end"] > b["start"] and b["end"] > a["end"]:
                a["start"] = b["start"]
                a["gene"] = "[%s^%s]"% (a["gene"], b["gene"])
                a["match"] = 1
                return a
            elif a["start"] > b["start"] and b["end"] > a["start"] and a["end"] > b["end"]:
                a["end"] = b["end"]
                a["gene"] = "[%s^%s]"% (a["gene"], b["gene"])
                a["match"] = 1
                return a
            elif a["start"] <= b["start"] and a["end"] >= b["end"]:
                a = b.copy()
                a["match"] = 1
                return a
            elif b["start"] <= a["start"] and b["end"] >= a["end"]:
                a["match"] = 1
                return a
            else:
                raise Exception("[OVERLAP]Unexcepted A B range: %s A[%s - %s] B[%s - %s]" % (a["chr"], a["start"], a["end"], b["start"], b["end"]))
        else:
            if "match" not in a:
                a["match"] = 0
            return a

    def get_append_area(b_a, b_b):
        a_append = []
        for f_a in b_a:
            f_a_l = [f_a]
            for f_b in b_b:
                f_a_l = get_a_left(f_a_l, f_b)
                if not f_a_l:
                    break
            if f_a_l:
                a_append += f_a_l

        if args.merge:
            a_append = merge(a_append)
        return a_append

    def get_overlap_area(b_a, b_b):
        a_overlap = []
        for f_a in b_a:
            f_overlap = f_a.copy()
            for f_b in b_b:
                f_overlap = get_ab_overlap(f_overlap, f_b)
            if f_overlap["match"] == 1:
                a_overlap.append(f_overlap)

        if args.merge:
            a_overlap = merge(a_overlap)
        return a_overlap

    def output_b(d, n):
        with open(os.path.join(args.dir_output, n), 'wb') as o:
            for line in d:
                o.write("%s\t%s\t%s\t%s\n" % (line["chr"], line["start"], line["end"], line["gene"]))

    bed_a = read_bed(args.bed_a, 'list')
    bed_b = read_bed(args.bed_b, 'list')

    bed_a_name = re.match('(.+)\.bed$', os.path.basename(args.bed_a)).group(1)
    bed_b_name = re.match('(.+)\.bed$', os.path.basename(args.bed_b)).group(1)

    print print_colors("• output ..."),
    output_b(get_append_area(bed_a, bed_b), "%s->%s_append" % (bed_a_name, bed_b_name))
    output_b(get_append_area(bed_b, bed_a), "%s->%s_miss" % (bed_a_name, bed_b_name))
    output_b(get_overlap_area(bed_a, bed_b), "%s->%s_overlap" % (bed_a_name, bed_b_name))
    print print_colors("OK!", 'green')

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='compare', formatter_class=RawTextHelpFormatter,
                                     description="• compare VCF\n"
                                                 "• compare BED")
    subparsers = parser.add_subparsers(dest='subparser_name', help='compare with different way')

    parser_a = subparsers.add_parser('vcf', help='compare vcf(.vcf/.xls) A -> B')
    parser_a.add_argument('sample_a', type=str, help='Specify path of variant file A')
    parser_a.add_argument('sample_b', type=str, help='Specify path of variant file B')
    parser_a.add_argument('dir_output', type=str, help='Specify directory of output')
    parser_a.add_argument('-c', '--cross_xls', action='store_true', help='Sample A is a .xls file from crossSNP')
    parser_a.add_argument('-t', '--ts_xls', action='store_true', help='Sample B is a .xls file from TS')
    parser_a.add_argument('-a', '--append_bed', type=str, help='Use append BED to filter Append')
    parser_a.add_argument('-m', '--miss_bed', type=str, help='Use miss BED to filter Miss')
    parser_a.set_defaults(func=compare_vcf)

    parser_b = subparsers.add_parser('bed', help='compare bed A -> B')
    parser_b.add_argument('bed_a', type=str, help='Specify path of bed file A')
    parser_b.add_argument('bed_b', type=str, help='Specify path of bed file B')
    parser_b.add_argument('dir_output', type=str, help='Specify directory of output')
    parser_b.add_argument('-m', '--merge', action='store_true', help='merge fragments if they got overlaps')
    parser_b.add_argument('-c', '--cross_xls', action='store_true', help='Sample A is a .xls file from crossSNP')
    parser_b.set_defaults(func=compare_bed)

    args = parser.parse_args()
    args.func()
