#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : checkMissing
# AUTHOR  : codeunsolved@gmail.com
# CREATED : November 28 2016
# VERSION : v0.0.1a

from __future__ import division
import os
import re
import json
import argparse
from argparse import RawTextHelpFormatter

import pysam
import xlwt

from base import print_colors
from base import handle_sap_id
from config import mysql_config
from database_connector import MysqlConnector

# CONFIG AREA #
check_pos = [["chr1", 11854476, 11854476, "MTHFR", "T"],
             ["chr1", 11856378, 11856378, "MTHFR", "G"],
             ["chr1", 20915701, 20915701, "CDA", "A"],
             ["chr1", 97915614, 97915614, "DPYD", "C"],
             ["chr1", 97981395, 97981395, "DPYD", "T"],
             ["chr1", 98348885, 98348885, "DPYD", "G"],
             ["chr2", 95539307, 95539307, "TEKT4", "A"],
             ["chr2", 95539313, 95539313, "TEKT4", "A"],
             ["chr2", 234668879, 234668879, "UGT1A10,UGT1A3,UGT1A4,UGT1A5,UGT1A6,UGT1A7,UGT1A8,UGT1A9", "C"],
             ["chr2", 234669144, 234669144, "UGT1A1", "G"],
             ["chr3", 14187449, 14187449, "XPC", "G"],
             ["chr3", 124456742, 124456742, "OPRT", "G"],
             ["chr6", 18130918, 18130918, "TPMT", "T"],
             ["chr6", 160113872, 160113872, "SOD2(MnSOD)", "A"],
             ["chr7", 55241705, 55241705, "EGFR", "T"],
             ["chr7", 55241707, 55241707, "EGFR", "G"],
             ["chr7", 55242475, 55242475, "EGFR", "G"],
             ["chr7", 55242506, 55242506, "EGFR", "T"],
             ["chr7", 55249005, 55249005, "EGFR", "G"],
             ["chr7", 55249012, 55249012, "EGFR", "C"],
             ["chr7", 55249071, 55249071, "EGFR", "C"],
             ["chr7", 55249092, 55249092, "EGFR", "G"],
             ["chr7", 55259515, 55259515, "EGFR", "T"],
             ["chr7", 55259524, 55259524, "EGFR", "T"],
             ["chr7", 87138645, 87138645, "ABCB1", "A"],
             ["chr7", 99361626, 99361626, "CYP3A4", "A"],
             ["chr7", 99367392, 99367392, "CYP3A4", "C"],
             ["chr7", 99367825, 99367825, "CYP3A4", "T"],
             ["chr7", 140453136, 140453136, "BRAF", "A"],
             ["chr10", 96741053, 96741053, "CYP2C9", "A"],
             ["chr10", 101563815, 101563815, "ABCC2(MRP2)", "G"],
             ["chr11", 4159457, 4159457, "RRM1", "A"],
             ["chr11", 4159466, 4159466, "RRM1", "G"],
             ["chr11", 67352689, 67352689, "GSTP1", "A"],
             ["chr11", 103418158, 103418158, "DYNC2H1(dist=67567),MIR4693(dist=302476)", "A"],
             ["chr12", 25380275, 25380275, "KRAS", "T"],
             ["chr12", 25398281, 25398281, "KRAS", "C"],
             ["chr12", 25398281, 25398281, "KRAS", "C"],
             ["chr12", 25398281, 25398281, "KRAS", "C"],
             ["chr12", 25398282, 25398282, "KRAS", "C"],
             ["chr12", 25398282, 25398282, "KRAS", "C"],
             ["chr12", 25398282, 25398282, "KRAS", "C"],
             ["chr12", 25398284, 25398284, "KRAS", "C"],
             ["chr12", 25398284, 25398284, "KRAS", "C"],
             ["chr12", 25398284, 25398284, "KRAS", "C"],
             ["chr12", 25398285, 25398285, "KRAS", "C"],
             ["chr12", 25398285, 25398285, "KRAS", "C"],
             ["chr12", 25398285, 25398285, "KRAS", "C"],
             ["chr16", 69745145, 69745145, "NQO1", "G"],
             ["chr16", 69748869, 69748869, "NQO1", "G"],
             ["chr19", 41512841, 41512841, "CYP2B6", "G"],
             ["chr19", 41515263, 41515263, "CYP2B6", "A"],
             ["chr19", 44055726, 44055726, "XRCC1", "T"],
             ["chr19", 44057574, 44057574, "XRCC1", "G"],
             ["chr19", 45854919, 45854919, "ERCC2", "T"],
             ["chr19", 45867259, 45867259, "ERCC2", "C"],
             ["chr19", 45923653, 45923653, "ERCC1", "A"],
             ["chr22", 42526694, 42526694, "CYP2D6", "G"]]

check_depth = [["chr22", 24376132, 24376622, "GSTT1"],
               ["chr22", 24376820, 24377002, "GSTT1"],
               ["chr22", 24379360, 24379512, "GSTT1"],
               ["chr22", 24381700, 24381792, "GSTT1"],
               ["chr22", 24384112, 24384312, "GSTT1"],
               ["chr18", 657646, 657673, "TYMS"]]


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
                if item[3] == p[4] and item[4] in stat:
                    if args.verbose: print print_colors("%d/%d Got %s-%s in vcf" % (i+1, cursor.rowcount, p, item[4]), 'green')
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
        print print_colors("• Check Pos ..."),
        if args.verbose: print "\n"

        pass_n = 0
        filter_n = 0
        remain_n = 0
        uncover_n = 0

        for p in check_pos:
            match_trigger = 0
            for pileupcolumn in sam.pileup(p[0], p[1]-1, p[2]): # must +1/-1 to pileup, maybe something like range().
                if pileupcolumn.pos == p[1]-1: # pileup using 0-based indexing
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
                    vcf_alt = vcf_filter([pipeline, sap_id, run_bn, p[0], p[1]], p, nt_stat)
                    append = vcf_alt["append"] if vcf_alt["append"] else ""
                    match = vcf_alt["match"] if vcf_alt["match"] else ""
                    if vcf_alt["filter"] == 2:
                        filter_n += 1
                        if args.verbose: print print_colors("[Filter] %s already called in vcf: %s" % (p, vcf_alt["match"]), 'red')
                    else:
                        alt_frequency = get_alt_freq(nt_stat, p[4], pileupcolumn.n)
                        if alt_frequency == "No mutation":
                            pass_n += 1
                            if args.verbose: print print_colors("[Pass] %s No mutation" % p, 'red')
                        else:
                            remain_n += 1
                            item = [sap_id, run_bn] + p +[nt_stat, alt_frequency, pileupcolumn.n, append, match]
                            check_pos_data.append(item)
                            if args.verbose: print item
                    break
            if not match_trigger:
                #raise Exception("No match - %s" % p)
                uncover_n += 1
                check_pos_data.append([sap_id, run_bn] + p + ["Uncovered"])
        print print_colors("Pass: %d, Filter: %d, Remain: %d/%d, Uncover: %d " % (pass_n, filter_n, remain_n, len(check_pos), uncover_n), 'grey'),
        print print_colors("OK!", 'green')

    # Check Depth
    if not args.skip_depth:
        print print_colors("• Check Depth ..."),
        if args.verbose: print "\n"

        filter_n = 0
        low_depth_n = 0
        deletion_n = 0

        for d in check_depth:
            depths = []
            high_depth = 0
            for pileupcolumn in sam.pileup(d[0], d[1]-1, d[2]):
                if pileupcolumn.pos in range(d[1]-1, d[2]+1):
                    if pileupcolumn.n > 10:
                        high_depth += 1
                    depths.append([pileupcolumn.pos, pileupcolumn.n])
            if depths == []:
                deletion_n += 1
                check_depth_data.append([sap_id, run_bn] + d + ["Deletion"])
            else:
                if high_depth == len(range(d[1]-1, d[2]+1)):
                    filter_n += 1
                    if args.verbose: print print_colors("[Filter] %s all depths > 10" % d, 'red')
                else:
                    low_depth_n += 1
                    check_depth_data.append([sap_id, run_bn] + d + [depths])
        print print_colors("Filter: %d, LowDepth: %d/%d, Deletion: %d/%d " % 
                           (filter_n, low_depth_n, len(check_depth), deletion_n, len(check_depth)), 'grey'),
        print print_colors("OK!", 'green')


def handle_autobox():
    pipeline = re.search('(_.+_?)$', args.dir_data).group(1)
    for sap in os.listdir(args.dir_data):
        dir_sap = os.path.join(args.dir_data, sap)
        if os.path.isdir(dir_sap):
            print print_colors("-{%s}" % sap, 'red')
            sample_id = handle_sap_id(sap)
            if os.path.isdir(dir_sap):
                for f in os.listdir(dir_sap):
                    if re.search('\.bam', f):
                        path_f = os.path.join(dir_sap, f)
                        samfile = pysam.AlignmentFile(path_f, "rb")
                        main(samfile, sample_id, args.run_bn, pipeline)
                        samfile.close()
    print "------------------\n" + print_colors("• output CheckMissing.xls to %s ..." % args.dir_data),
    output(args.dir_data)
    print print_colors("OK!", 'green')


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='check Missing', formatter_class=RawTextHelpFormatter,
                                     description="• check certain pos mutation\n"
                                                 "• check certain region lowdepth or deletion\n")
    subparsers = parser.add_subparsers(help='Check missing with different source')

    parser_a = subparsers.add_parser('autobox', help='from autobox')
    parser_a.add_argument('dir_data', type=str, help='Specify directory of data')
    parser_a.add_argument('project', type=str, help='Specify Project')
    parser_a.add_argument('run_bn', type=str, help='Specify RUN batch No.')
    parser_a.add_argument('-kp', '--skip_pos', action='store_true', help="skip Check Pos")
    parser_a.add_argument('-kd', '--skip_depth', action='store_true', help="skip Check Depth")
    parser_a.add_argument('-v', '--verbose', action='store_true', help='Show debug')
    parser_a.set_defaults(func=handle_autobox)

    args = parser.parse_args()

    # handle table belonging
    if args.project == '56gene':
        table_vcf = '56gene_vcf'
    elif args.project in ['42geneLung', '42gene']:
        table_vcf = '42gene_vcf'
    elif args.project == 'BRCA':
        table_vcf = 'BRCA_vcf'
    elif args.project == 'ZS-BRCA':
        table_vcf = 'ZS_BRCA_vcf'
    else:
        raise Exception('Unknown Project: %s' % args.project)

    check_pos_data = [["Sample_id", "RUN", "Chr", "Pos_start", "Pos_end", "Gene", "Ref", "Alt", "Frequency", "Depth", "VCF_Append", "VCF_Match"]]
    check_depth_data = [["Sample_id", "RUN", "Chr", "Pos_start", "Pos_end", "Gene", "Depth"]]

    m_con = MysqlConnector(mysql_config, 'TopgenNGS')
    args.func()
    m_con.done()
