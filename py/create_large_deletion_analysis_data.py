#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : create_large_deletion_analysis_data
# AUTHOR  : codeunsolved@gmail.com
# CREATED : November 2 2016
# VERSION : v0.0.1a

from __future__ import division
import os
import re
import json
import argparse

import pandas

from config import mysql_config
from lib.base import read_bed
from lib.base import clean_output
from lib.base import print_colors
from lib.database_connector import MysqlConnector


def read_sample_reads():
    path_reads_stat = os.path.join(dir_data, 'reads_statistics-reads')
    return pandas.DataFrame.from_csv(path_reads_stat, header=0, sep='\t')


def init_amplicon_data(sap_name):
    def init_amplicon_cover():
        amplicon_cover = {}
        for f_key in frag_details:
            amplicon_cover[f_key] = {"amp_name": f_key,
                                     "chr_num": re.match('chr(.+)', frag_details[f_key][0]).group(1),
                                     "gene_name": frag_details[f_key][1],
                                     "pos_s": frag_details[f_key][2], "pos_e": frag_details[f_key][3],
                                     "len": frag_details[f_key][3] - frag_details[f_key][2] + 1,
                                     "aver_depth": None, "max_depth": None, "min_depth": None,
                                     "x_labels": [], "depths": [],
                                     "reads": None
                                     }
        return amplicon_cover

    amplicon_data = {"sample_name": sap_name,
                     "amp_cover": init_amplicon_cover(),
                     "deletion_gap": [],
                     "absent_amp": [],
                     "ignored_amp": {},
                     "data_ver": "v0.0.1"
                     }
    return amplicon_data


def output_json(data, p_json):
    with open(p_json, 'wb') as o:
        o.write(json.dumps(data))


def import_data(data):
    m_con = MysqlConnector(mysql_config, 'TopgenNGS')
    insert_g = ("INSERT INTO BRCA_LargeDeletion "
                "(SAP_id, RUN_bn, LargeDeletion, Ignored, AmpData) "
                "VALUES (%s, %s, %s, %s, %s)")
    for d in data:
        if m_con.query("SELECT id FROM BRCA_LargeDeletion "
                       "WHERE SAP_id=%s AND RUN_bn=%s",
                       d[:2]).rowcount == 1:
            print "=>update %s" % d[2:]
            m_con.query("UPDATE BRCA_LargeDeletion "
                        "SET LargeDeletion=%s, Ignored=%s, AmpData=%s "
                        "WHERE SAP_id=%s AND RUN_bn=%s",
                        (d[2], d[3], d[4], d[0], d[1]))
            m_con.cnx.commit()
        else:
            print "=>insert %s" % d
            m_con.insert(insert_g, d)
    m_con.done()

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='create sample cover data')
    parser.add_argument('dir_data', type=str, help="path of data's directory")
    parser.add_argument('path_bed', type=str, help="path of bed file")

    parser.add_argument('-g', '--deletion_gap', metavar='N', type=int, default=20, help="set deletion gap")
    parser.add_argument('-d', '--depth_cutoff', metavar='N', type=int, default=60, help="set depth cutoff(%%)")
    parser.add_argument('-r', '--reads_counts_at_least', metavar='N', type=int, default=30, help="set at least reads counts")

    args = parser.parse_args()

    dir_data = args.dir_data
    path_bed = args.path_bed
    dir_output = os.path.join(r'/Users/codeunsolved/Sites/topgen-dashboard/data', os.path.basename(dir_data))

    depth_cutoff = args.depth_cutoff / 100

    print print_colors("clean dir output ..."),
    clean_output(dir_output, "large_deletion")
    print print_colors("OK!", 'green')
    frag_details = read_bed(path_bed)
    frag_details_sorted = sorted(frag_details.iteritems(), key=lambda d: (d[1][0], d[1][2]))
    reads_stat = read_sample_reads()

    dir_name = os.path.basename(dir_data)
    # handle project
    if re.search('BRCA', dir_name):
        project = 'BRCA'
    elif re.search('onco', dir_name):
        project = '56gene'
    else:
        project = 'unknown'
    # handle run batch number
    if re.match('BRCA|onco', dir_name):
        run_bn = re.match('(?:BRCA|onco)(.+)', dir_name).group(1)
    else:
        run_bn = dir_name

    sample_num = 0
    sample_cover = []
    mysql_data = []
    for f in os.listdir(dir_data):
        if re.match('^.+\.depth$', f):
            print print_colors("<No.%d %s>" % (sample_num + 1, f))
            sample_num += 1

            # handle sample name
            file_name = re.match('(.+)\.depth', f).group(1)
            if re.search('_S\d+', file_name):
                sample_name = re.match('(.+)_S\d+', file_name).group(1)
            elif re.search('autoBox', file_name):
                sample_name = re.match('(.+)_20\d{2}_\d{2}_\d{2}', file_name).group(1)
            else:
                sample_name = file_name

            with open(os.path.join(dir_data, f), 'rb') as depth_file:
                amp_data = init_amplicon_data(sample_name)
                depth_digest_stat = {}
                deletion_gap = {}
                for i, line_depth in enumerate(depth_file):
                    chr_n = re.match('([^\t]+)\t', line_depth).group(1)
                    pos = int(re.match('[^\t]+\t([^\t]+\t)', line_depth).group(1))
                    depth = int(re.match('(?:[^\t]+\t){2}([^\t\r\n]+)', line_depth).group(1))
                    for key, value in frag_details_sorted:
                        if key not in depth_digest_stat:
                            depth_digest_stat[key] = {"sum": 0, "max": None, "min": None, "0x_depth": 0}
                        amp_data['amp_cover'][key]['reads'] = reads_stat[sample_name][key] / 2
                        if chr_n == value[0] and value[2] <= pos <= value[3]:
                            depth_digest_stat[key]['sum'] += depth
                            if depth > depth_digest_stat[key]['max'] or not depth_digest_stat[key]['max']:
                                depth_digest_stat[key]['max'] = depth
                            if depth < depth_digest_stat[key]['min'] or not depth_digest_stat[key]['min']:
                                depth_digest_stat[key]['min'] = depth
                            if depth == 0:
                                depth_digest_stat[key]['0x_depth'] += 1

                            amp_data['amp_cover'][key]['x_labels'].append(pos)
                            amp_data['amp_cover'][key]['depths'].append(depth)

                            # handle deletion gap
                            if amp_data['amp_cover'][key]['reads'] >= args.reads_counts_at_least:
                                if depth <= amp_data['amp_cover'][key]['reads'] * depth_cutoff:
                                    if key not in deletion_gap:
                                        deletion_gap[key] = {'trigger': 0, 'gaps': []}
                                    if deletion_gap[key]['trigger'] == 0:
                                        deletion_gap[key]['gaps'].append({'key': key,
                                                                          'reads_counts': amp_data['amp_cover'][key]['reads'],
                                                                          'len': 0, 'pos': [], 'depth': [],
                                                                          'zero_pos': []})
                                    deletion_gap[key]['gaps'][-1]['len'] += 1
                                    deletion_gap[key]['gaps'][-1]['pos'].append(pos)
                                    deletion_gap[key]['gaps'][-1]['depth'].append(depth)
                                    if depth == 0:
                                        deletion_gap[key]['gaps'][-1]['zero_pos'].append(pos)
                                    deletion_gap[key]['trigger'] += 1
                                else:
                                    if key in deletion_gap:
                                        deletion_gap[key]['trigger'] = 0
                            else:
                                if key not in amp_data['ignored_amp']:
                                    print print_colors('=>Ignored [%s]%s' % (amp_data['amp_cover'][key]['reads'], key), 'yellow')
                                    amp_data['ignored_amp'][key] = amp_data['amp_cover'][key]['reads']

                for key in amp_data['amp_cover']:
                    # add amp info (max, min, aver depth)
                    if len(amp_data['amp_cover'][key]["x_labels"]) != 0:
                        amp_data['amp_cover'][key]['aver_depth'] = round(
                            depth_digest_stat[key]['sum'] / amp_data['amp_cover'][key]['len'] * 100, 2
                        )
                        amp_data['amp_cover'][key]['max_depth'] = depth_digest_stat[key]['max']
                        amp_data['amp_cover'][key]['min_depth'] = depth_digest_stat[key]['min']
                        # add absent amplicon
                        if depth_digest_stat[key]['0x_depth'] == amp_data['amp_cover'][key]['len']:
                            amp_data['absent_amp'].append(key)
                    else:
                        # add absent amplicon
                        amp_data['absent_amp'].append(key)

                # filter deletion gap
                for key, value in deletion_gap.iteritems():
                    pop_i = []
                    for i, gap in enumerate(value['gaps']):
                        if gap['len'] < args.deletion_gap:
                            pop_i.insert(0, i)
                    for i in pop_i:
                        print print_colors("Popped %s" % gap, 'red')
                        value['gaps'].pop(i)
                    amp_data['deletion_gap'] += value['gaps']
                    print value['gaps']

                path_json = os.path.join(os.path.join(dir_output, "large_deletion"), "%s.json" % amp_data['sample_name'])

                mysql_data.append([sample_name, run_bn, len(deletion_gap), len(amp_data['ignored_amp']), path_json])
                print print_colors("• output data ..."),
                output_json(amp_data, path_json)
                print print_colors("OK!", 'green')

    print print_colors("• import data ...")
    import_data(mysql_data)
    print print_colors("OK!", 'green')
