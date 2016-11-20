#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : sql_Clinvar
# AUTHOR  : codeunsolved@gmail.com
# CREATED : September 7 2016
# VERSION : v0.0.1a

import os
import re
import time

from base import parse_vcf
from config import mysql_config
from database_connector import MysqlConnector

# CONFIG AREA #
dir_vcf = r'/Users/codeunsolved/Downloads/NGS-Data/Report-fusion_gene/=TEMP=/BRCA160320/normVCF'
dir_output = r'/Users/codeunsolved/Downloads/NGS-Data/Report-fusion_gene/=TEMP=/BRCA160320/clinvar-match'
vcf_suffix = 'step2\.vcf'


def query_clinvar(term):
    query_g = ("SELECT Chr, Pos_S, Pos_E, Ref, Alt, CLINSIG FROM hg19_clinvar_20160302_origin "
               "WHERE Chr=%s AND Pos_S=%s AND Ref=%s AND Alt=%s")
    return m_con.query(query_g, term)


def output_clinvar_match(data):
    with open(os.path.join(dir_output, 'output-clinvar-match.log'), 'wb') as output:
        for row in data:
            output.write("%s\n" % "\t".join([str(x) for x in row]))

if __name__ == '__main__':
    time_start = time.time()
    m_con = MysqlConnector(mysql_config, 'TopgenNGS')
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
    print "====== Done ======\nTotal VCF: %d\t Time: %s" % (len(vcf_files), time.time() - time_start)
