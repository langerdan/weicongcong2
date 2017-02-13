#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : checkMissing
# AUTHOR  : codeunsolved@gmail.com
# CREATED : November 28 2016
# VERSION : v0.0.1
# UPDATE  : [v0.0.1] December 13 2016
# 1. Check Pos extend to 2414 point and seperate to a file(check_pos_v0.2);
# 2. add filter - Alt frequency < 0.5%;
# 3. add filter - Not include target Alt type;
# remain problems:
# (1). can not check indel;

from __future__ import division
import os
import re
import json
import argparse

import pysam
import xlwt

from config import mysql_config
from lib.base import color_term
from lib.base import handle_table
from lib.base import handle_sap_id
from lib.base import handle_run_bn
from lib.base import handle_project
from lib.database_connector import MysqlConnector


def output(dir_o):
    def set_style(height=210, bold=False, background_color='aqua', font_color='black', name='Microsoft YaHei UI'):
        style = xlwt.XFStyle()
        # font
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.colour_index = xlwt.Style.colour_map[font_color]
        font.height = height
        style.font = font
        # background color
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map[background_color]
        style.pattern = pattern
        return style

    path_output = os.path.join(dir_o, "CheckMissing.xls")
    workbook = xlwt.Workbook(style_compression=2)

    sheet1 = workbook.add_sheet("Check Pos", cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet("Check Depth", cell_overwrite_ok=True)

    # sheet table header
    for i, t in enumerate(check_pos_data[0]):
        sheet1.write(0, i, t, set_style(220, True))
    for i, t in enumerate(check_depth_data[0]):
        sheet2.write(0, i, t, set_style(220, True))

    # sheet table content
    for i, row in enumerate(check_pos_data[1:]):
        for j, c in enumerate(row):
            sheet1.write(i+1, j, str(c))
    for i, row in enumerate(check_depth_data[1:]):
        for j, c in enumerate(row):
            sheet2.write(i+1, j, str(c))
    workbook.save(path_output)


def get_check(path_check):
    check = []
    with open(path_check, 'rb') as cp:
        for line in cp:
            if re.match('#', line):
                continue
            check.append(line.strip().split('\t'))
    return check


def query_vcf(term):
    query_g = ("SELECT Chr, Pos, RS_id, Ref, Alt FROM {} "
               "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos=%s".format(table_vcf))
    return m_con.query(query_g, term)


def main(sam, sap_id, run_bn, pipeline):
    def get_alt_freq(stat, ref, depth):
        alt_freq = {}
        for k in stat:
            if k is not ref:
                alt_freq[k] = round(stat[k]/depth, 4)
        if alt_freq == {}:
            return "No mutation"
        else:
            return alt_freq

    def vcf_filter(term, p, stat):
        v = {"match": [], "append": [], "filter": 0}
        cursor = query_vcf(term)
        if cursor.rowcount:
            for i, item in enumerate(cursor.fetchall()):
                if str(item[3]) == ref and str(item[4]) in stat:
                    if args.verbose: print color_term("%d/%d Got %s > %s in vcf" %
                                                      (i+1, cursor.rowcount, '-'.join(p[:4] + [ref]), str(item[4])), 'green')
                    v["match"].append([str(x) for x in item[2:]])
                    continue
                else:
                    v["append"].append(', '.join([str(x) for x in item]))
            if v["match"] != [] and len(v["match"]) == len(stat)-1:
                v["filter"] |= 2
            if v["append"] != []:
                v["filter"] |= 1
        return v

    # Check Pos
    if not args.skip_pos:
        print color_term("• Check Pos ..."),
        if args.verbose or args.verbose2: print ""

        pass_n = 0
        filter_n = 0
        remain_n = 0
        uncover_n = 0

        check_pos = get_check(os.path.join(os.path.dirname(__file__), 'check/check_pos_v0.2'))
        for p in check_pos:
            match_trigger = 0

            chr_ = p[0]
            pos_s = int(p[1])
            pos_e = int(p[2])
            ref = p[7]
            alt = p[8]

            for pileupcolumn in sam.pileup(chr_, pos_s-1, pos_e): # must +1/-1 to pileup, maybe something like range().
                if pileupcolumn.pos == pos_s-1: # pileup using 0-based indexing
                    #print "Pos: %s Depth: %s" % (pileupcolumn.pos, pileupcolumn.n)
                    nt_stat = {}
                    match_trigger = 1
                    for pileupread in pileupcolumn.pileups:
                        if not pileupread.is_del and not pileupread.is_refskip:
                            # query position is None if is_del or is_refskip is set.
                            nt = pileupread.alignment.query_sequence[pileupread.query_position]
                            if nt not in nt_stat:
                                nt_stat[nt] = 1
                            else:
                                nt_stat[nt] += 1
                    alt_frequency = get_alt_freq(nt_stat, ref, pileupcolumn.n)

                    vcf_alt = vcf_filter([pipeline, sap_id, run_bn, chr_, pos_s], p, nt_stat)
                    append = vcf_alt["append"] if vcf_alt["append"] else ""
                    match = vcf_alt["match"] if vcf_alt["match"] else ""
                    # filter - VCF matched all alt type
                    if vcf_alt["filter"] == 2:
                        filter_n += 1
                        if args.verbose: print color_term("[FILTER-MATCH] Alt: %s already called in vcf: %s" % (alt_frequency.keys(), vcf_alt["match"]), 'red')
                        if args.debug_filter: check_pos_data.append([sap_id, run_bn] + p[:-1] + 
                                                                    ["[FILTER-MATCH]" + str(nt_stat), alt_frequency, pileupcolumn.n, append, match])
                    else:
                        if alt_frequency == "No mutation":
                            pass_n += 1
                            if args.verbose: print color_term("[Pass] %s No mutation" % '-'.join(p[:4] + [ref]), 'red')
                        else:
                            # filter - Alt frequency < 0.5%
                            low_freq = []
                            for k_a in alt_frequency:
                                if alt_frequency[k_a] < 0.005:
                                    low_freq.append(k_a)
                            if set(low_freq + [x[-1] for x in match]) == set(alt_frequency.keys()):
                                filter_n += 1
                                if args.verbose: print color_term("[FILTER-LOWFREQ] except matches(%s) in VCF, all alt freq(%s) < 0.5%%" %
                                                                  ([x[-1] for x in match], [alt_frequency[x] for x in low_freq]), 'red')
                                if args.debug_filter: check_pos_data.append([sap_id, run_bn] + p[:-1] + 
                                                                            ["[FILTER-LOWFREQ]" + str(nt_stat), alt_frequency, pileupcolumn.n, append, match])
                            # filter - Not include target Alt type
                            elif alt in ['A', 'T', 'G', 'C'] and alt not in alt_frequency:
                                filter_n += 1
                                if args.verbose: print color_term("[FILTER-NO_TARGET_ALT] %s no target alt type: %s" % ('-'.join(p[:4]), alt), 'red')
                                if args.debug_filter: check_pos_data.append([sap_id, run_bn] + p[:-1] + 
                                                                            ["[FILTER-NO_TARGET_ALT]" + str(nt_stat), alt_frequency, pileupcolumn.n, append, match])
                            else:
                                remain_n += 1
                                item = [sap_id, run_bn] + p[:-1] + [nt_stat, alt_frequency, pileupcolumn.n, append, match]
                                check_pos_data.append(item)
                                if args.verbose2: print item
                    break
            if not match_trigger:
                #raise Exception("No match - %s" % p)
                uncover_n += 1
                check_pos_data.append([sap_id, run_bn] + p + ["Uncovered"])
        print color_term("Pass: %d, Filter: %d, Remain: %d/%d, Uncover: %d " % (pass_n, filter_n, remain_n, len(check_pos), uncover_n), 'grey'),
        print color_term("OK!", 'green')

    # Check Depth
    if not args.skip_depth:
        print color_term("• Check Depth ..."),
        if args.verbose or args.verbose2: print ""

        filter_n = 0
        low_depth_n = 0
        deletion_n = 0

        check_depth = get_check(os.path.join(os.path.dirname(__file__), 'check/check_depth_v0.1'))
        for d in check_depth:
            depths = []
            high_depth = 0

            chr_ = d[0]
            pos_s = int(d[1])
            pos_e = int(d[2])

            for pileupcolumn in sam.pileup(chr_, pos_s-1, pos_e):
                if pileupcolumn.pos in range(pos_s-1, pos_e+1):
                    if pileupcolumn.n > 10:
                        high_depth += 1
                    depths.append([pileupcolumn.pos, pileupcolumn.n])
            if depths == []:
                deletion_n += 1
                check_depth_data.append([sap_id, run_bn] + d + ["Deletion"])
            else:
                if high_depth == len(range(pos_s-1, pos_e+1)):
                    filter_n += 1
                    if args.verbose: print color_term("[Filter] %s all depths > 10" % d, 'red')
                else:
                    low_depth_n += 1
                    check_depth_data.append([sap_id, run_bn] + d + [depths])
        print color_term("Filter: %d, LowDepth: %d/%d, Deletion: %d/%d " %
                         (filter_n, low_depth_n, len(check_depth), deletion_n, len(check_depth)), 'grey'),
        print color_term("OK!", 'green')


def handle_autobox():
    pipeline = re.search('\d(_.+_?)$', dir_data_name).group(1)
    for sap in os.listdir(dir_data):
        dir_sap = os.path.join(dir_data, sap)
        if os.path.isdir(dir_sap):
            print color_term("-{%s}" % sap, 'red')
            sample_id = handle_sap_id(sap)
            if os.path.isdir(dir_sap):
                for f in os.listdir(dir_sap):
                    if re.search('\.bam', f):
                        path_f = os.path.join(dir_sap, f)
                        samfile = pysam.AlignmentFile(path_f, "rb")
                        main(samfile, sample_id, run_bn, pipeline)
                        samfile.close()
    print "------------------\n• output CheckMissing.xls to %s ..." % dir_data,
    output(dir_data)
    print color_term("OK!", 'green')


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='checkMissing', formatter_class=argparse.RawTextHelpFormatter,
                                     description="• check certain pos mutation\n"
                                                 "• check certain region lowdepth or deletion\n")
    subparsers = parser.add_subparsers(dest='subparser_name', help='Check missing with different source')

    parser_a = subparsers.add_parser('autobox', help='from autobox')
    parser_a.add_argument('dir_data', type=str, help='Specify directory of data')
    parser_a.add_argument('-p', '--project', type=str, help='Specify Project')
    parser_a.add_argument('-r', '--run_bn', type=str, help='Specify RUN batch No.')
    parser_a.add_argument('-kp', '--skip_pos', action='store_true', help="Skip Check Pos")
    parser_a.add_argument('-kd', '--skip_depth', action='store_true', help="Skip Check Depth")
    parser_a.add_argument('-df', '--debug_filter', action='store_true', help="Debug filter")
    parser_a.add_argument('-v', '--verbose', action='store_true', help='Show debug')
    parser_a.add_argument('-v2', '--verbose2', action='store_true', help='Show debug level 2')
    parser_a.set_defaults(func=handle_autobox)

    args = parser.parse_args()

    dir_data = args.dir_data
    dir_data_name = os.path.basename(dir_data)

    # handle Project
    if args.project:
        project = args.project
    else:
        project = handle_project(dir_data_name)
    # handle RUN batch No.
    if args.run_bn:
        run_bn = args.run_bn
    elif args.subparser_name == 'autobox':
        run_bn = re.match("%s(\d+)" % project, dir_data_name).group(1)
    # handle table belonging
    project_table = handle_table(project)
    table_vcf = project_table['vcf']
    table_anno = project_table['anno']

    check_pos_data = [["Sample_id", "RUN", "Chr", "Pos_start", "Pos_end", "Gene", 
                       "Accession_number", "CDS_mut_syntax", "Strand", "Ref", "Alt", 
                       "Frequency", "Depth", "VCF_Append", "VCF_Match"]]
    check_depth_data = [["Sample_id", "RUN", "Chr", "Pos_start", "Pos_end", "Gene", 
                         "Accession_number", "CDS_mut_syntax", "Strand", "Depth"]]

    m_con = MysqlConnector(mysql_config, 'TopgenNGS')
    args.func()
    m_con.done()
