#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : sqlClinvar_v0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : September 7 2016

import os
import re
import time
from Mysql_Connector import MysqlConnector
from mysql_config import config

dir_vcf = r'/Users/codeunsolved/Downloads/NGS-Data/Report-fusion_gene/=TEMP=/BRCA160320/normVCF'
dir_output = r'/Users/codeunsolved/Downloads/NGS-Data/Report-fusion_gene/=TEMP=/BRCA160320/clinvar-match'
vcf_suffix = 'step2\.vcf'


def parse_vcf(p_vcf):
    vcf_body = []
    with open(p_vcf, 'rb') as r_obj:
        ver = None
        for line_no, line in enumerate(r_obj):
            if line_no == 0:
                ver = re.match('##fileformat=VCFv(.+)[\r\n]', line).group(1)
            if re.match('#', line):
                continue
            if ver == "4.1":
                chr_n = re.match('chr([^\t]+)\t', line).group(1)
                pos = int(re.match('[^\t]+\t([^\t]+)\t', line).group(1))
                id_snp = re.match('(?:[^\t]+\t){2}([^\t]+)\t', line).group(1)
                ref = re.match('(?:[^\t]+\t){3}([^\t]+)\t', line).group(1)
                alt = re.match('(?:[^\t]+\t){4}([^\t]+)\t', line).group(1)
                qual = re.match('(?:[^\t]+\t){5}([^\t]+)\t', line).group(1)
                q_filter = re.match('(?:[^\t]+\t){6}([^\t]+)\t', line).group(1)
                info = re.match('(?:[^\t]+\t){7}([^\t]+)\t', line).group(1)
                format_key = re.match('(?:[^\t]+\t){8}([^\t]+)\t', line).group(1)
                format_value = re.match('(?:[^\t]+\t){9}([^\t]+)[\r\n]', line).group(1)
                vcf_body.append([chr_n, pos, id_snp, ref, alt, qual, q_filter, info, format_key, format_value])
    return vcf_body


def query_clinvar(data):
    query_g = ("SELECT * FROM hg19_clinvar_20160302_origin "
               "WHERE Chr=%s AND Pos_S=%s AND Ref=%s AND Alt=%s")
    return m_con.query(query_g, data)


def output_clinvar_match(data):
    with open(os.path.join(dir_output, 'output-clinvar-match_2.log'), 'wb') as w_obj:
        for row in data:
            w_obj.write("%s\n" % "\t".join([str(x) for x in row]))


time_start = time.time()
m_con = MysqlConnector(config, 'TopgenNGS')
output = []
vcf_files = os.listdir(dir_vcf)
for vcf_file in vcf_files:
    if re.search('^[\dWD].+%s$' % vcf_suffix, vcf_file):
        print "=>%s" % vcf_file
        path_vcf = os.path.join(dir_vcf, vcf_file)
        vcf = parse_vcf(path_vcf)
        for variant in vcf:
            print "\t%s-%s-%s-%s" % (variant[0], variant[1], variant[3], variant[4])
            cursor = query_clinvar((variant[0], variant[1], variant[3], variant[4]))
            if cursor.rowcount:
                for each in cursor:
                    print "\t\t%s" % [str(x) for x in each]
                    if variant[2] != '.':
                        output.append([vcf_file, "match+", 1] + variant[:5] + list(each))
                    else:
                        output.append([vcf_file, "append", 1] + variant[:5] + list(each))
            else:
                print "\t\tNone"
                if variant[2] != '.':
                    output.append([vcf_file, "miss", 0] + variant[:5] + list(each))
                else:
                    output.append([vcf_file, "match-", 0] + variant[:5] + list(each))
m_con.done()
output_clinvar_match(output)
print "====== Done =======\nTotal VCF: %d\t Time: %s" % (len(vcf_files), time.time() - time_start)
