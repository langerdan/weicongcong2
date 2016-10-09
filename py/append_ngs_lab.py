#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : append_NGS_lab
# AUTHOR  : codeunsolved@gmail.com
# CREATED : September 29 2016
# VERSION : v0.0.1a

import os
import re
import sys

from database_connector import MysqlConnector
from config import mysql_config

dir_data = r'/Users/codeunsolved/Downloads/NGS-Data'
project = sys.argv[1]

already_had = {
    "BRCA": ['BRCA160107', 'BRCA160313', 'BRCA160320', 'BRCA160406', 'BRCA160408', 'BRCA160427', 'BRCA160517',
             'BRCA160601', 'BRCA160708', 'BRCA160724', 'BRCA160724-2', 'BRCA160727', 'BRCA160811', 'BRCA160819',
             'BRCA160824', 'BRCA160830', 'BRCA160906', 'BRCA160913', 'BRCA160919', 'BRCA160925', 'BRCA160929', 
             'BRCA160930'],
    "onco": ['onco160719+20', 'onco160729', 'onco160802', 'onco160804', 'onco160811', 'onco160813', 'onco160815',
             'onco160819', 'onco160824', 'onco160830', 'onco160830-42gene', 'onco160906', 'onco160913-42gene',
             'onco160919', 'onco160919-42gene', 'onco160920', 'onco160920-42gene', 'onco160925', 'onco160925-42gene', 
             'onco160928', 'onco160928-42gene', 'onco160929', 'onco160929-42gene', 'onco160930', 'onco160930-42gene']
}


def output_csv(data):
    with open('/Users/codeunsolved/Downloads/NGS-Data/DB/%s_lab-2.csv' % project, 'wb') as output:
        for row in data:
            output.write(',%s\n' % row)


def import_lab(data):
    if project == "onco":
        table = "56gene_lab"
    elif project == "BRCA":
        table = "BRCA_lab"

    m_con = MysqlConnector(mysql_config, 'TopgenNGS')
    insert_g = ("INSERT INTO {0} "
                "(`SAP_id`, `RUN_bn`) "
                "VALUES (%s, %s)".format(table))
    for item in data:
        item = item.split(',')
        if m_con.query("SELECT id FROM {0} "
                       "WHERE SAP_id=%s AND RUN_bn=%s".format(table),
                       (item[0], item[22])).rowcount == 1:
            print "=>record existed! ignore..."
        else:
            print "=>insert %s" % item
            m_con.insert(insert_g, (item[0], item[22]))
    m_con.done()


if __name__ == '__main__':
    proj_table = {}
    for dir_d in os.listdir(dir_data):
        dir_run = os.path.join(dir_data, dir_d)
        if re.match('%s' % project, dir_d) and os.path.isdir(dir_run) and dir_d not in already_had[project]:
            print "=>%s" % dir_run
            run_bn = re.match('%s(.+)' % project, dir_d).group(1)
            proj_table[run_bn] = []
            for file in os.listdir(dir_run):
                if re.search('(?!sort)\.bam$', file):
                    basename = re.match('(.+)\.bam', file).group(1)
                    if re.search('_S\d+', basename):
                        basename = re.match('(.+)_S\d+', file).group(1)
                    if re.search('autoBox', basename):
                        basename = re.match('(.+)_20[12]\d_\d\d_\d\d', file).group(1)
                    proj_table[run_bn].append(basename)
            print proj_table[run_bn]

    table_data = []
    proj_table_sorted = sorted(proj_table.iteritems(), key=lambda d: d[0])
    for key, value in proj_table_sorted:
        for sample_id in value:
            table_data.append('%s,,,0000-00-00,,,,,0000-00-00,,,,,,,,,,,,,0000-00-00,%s,,,,,,INIT' % (sample_id, key))
    output_csv(table_data)
    import_lab(table_data)
