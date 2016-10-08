#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : anno_VCF
# AUTHOR  : codeunsolved@gmail.com
# CREATED : September 18 2016
# VERSION : v0.0.1a

import os
import re
import sys
import json
import time

from base import clean_output
from base import parse_vcf
from database_connector import MysqlConnector
from config import mysql_config

dir_vcf = sys.argv[1]
dir_output = sys.argv[2]
vcf_suffix = 'step2\.vcf'
table_head = ["Chr", "Start", "End", "Ref", "Alt", "Clinvar"]


def query_clinvar(data):
    query_g = ("SELECT Chr, Pos_S, Pos_E, Ref, Alt, CLINSIG FROM hg19_clinvar_20160302_origin "
               "WHERE Chr=%s AND Pos_S=%s AND Ref=%s AND Alt=%s")
    return m_con.query(query_g, data)


def output_anno(data, filename):
    with open(os.path.join(dir_output_vcf, '%s.anno' % filename), 'wb') as anno_w:
        anno_w.write(json.dumps(data))


def input_mysql(data):
    insert_g = ("INSERT INTO ANNO "
                "(Project, SAP_id, RUN_bn, Path) "
                "VALUES (%s, %s, %s, %s)")
    for d in data:
        if m_con.query("SELECT id FROM ANNO "
                       "WHERE Project=%s AND SAP_id=%s AND RUN_bn=%s",
                       d[:3]).rowcount == 1:
            print "=>record existed!\n=>update %s" % d[3]
            m_con.query("UPDATE ANNO "
                        "SET Path=%s "
                        "WHERE Project=%s AND SAP_id=%s AND RUN_bn=%s",
                        (d[3], d[0], d[1], d[2]))
            m_con.cnx.commit()
        else:
            print "=>insert %s" % d
            m_con.insert(insert_g, d)

if __name__ == '__main__':
    clean_output(dir_output, "annotation")
    time_start = time.time()

    data_basename = os.path.basename(os.path.dirname(dir_vcf))
    if re.search('BRCA', data_basename):
        project = 'BRCA'
    elif re.search('onco', data_basename):
        project = '56gene'
    else:
        project = 'unknown'
    run_bn = data_basename
    if re.match('BRCA|onco', run_bn):
        run_bn = re.match('(?:BRCA|onco)(.+)', run_bn).group(1)

    m_con = MysqlConnector(mysql_config, 'TopgenNGS')
    mysql_data = []

    dir_output_vcf = os.path.join(dir_output, "annotation")
    vcf_files = os.listdir(dir_vcf)

    i = 0
    for vcf_file in vcf_files:
        if re.search('^.+%s$' % vcf_suffix, vcf_file):
            i += 1
            print "=>%s" % vcf_file

            sap_id = re.match('(.+)%s$' % vcf_suffix, vcf_file).group(1)
            if re.search('_S\d+', sap_id):
                sap_id = re.match('(.+)_S', sap_id).group(1)
            output = [table_head]

            path_vcf = os.path.join(dir_vcf, vcf_file)
            vcf = parse_vcf(path_vcf)

            for variant in vcf:
                variant_anno = []
                print "\t%s-%s-%s-%s" % (variant[0], variant[1], variant[3], variant[4])
                variant_anno = [variant[0], variant[1], variant[1], variant[3], variant[4]]

                # annotate clinvar
                cursor = query_clinvar((variant[0], variant[1], variant[3], variant[4]))
                if cursor.rowcount:
                    row = cursor.fetchone()
                    print "\t\t{Clinvar}%s" % [str(x) for x in row]
                    variant_anno.append(list(row)[-1])
                    if cursor.rowcount > 1:
                        print "\t\t{Clinvar} [WARNING] multiple matches!"
                else:
                    variant_anno.append("")
                output.append(variant_anno)
            output_anno(output, sap_id)
            mysql_data.append([project, sap_id, run_bn, "data/%s/annotation/%s.anno" % (data_basename, sap_id)])

    print "insert data..."
    input_mysql(mysql_data)
    print "OK!"
    m_con.done()
    print "====== Done ======\nTotal VCF: %d\t Time: %ss" % (i, time.time() - time_start)
