#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : pullData
# AUTHOR  : codeunsolved@gmail.com
# CREATED : November 21 2016
# VERSION : v0.0.1
# UPDATE  : [v0.0.1] December 20 2016
# 1. change name from 'pullMiSeq' to 'pullData';
# 2. add subparser{autobox};
# 3. use rsync to transmit data；

from __future__ import division
import os
import re
import argparse

from lib.base import execute_cmd
from lib.base import color_term
from lib.base import handle_sap_id


def get_size(path_file):
    file_size = os.path.getsize(path_file)
    return str(round(file_size / 1024 / 1024, 2)) + 'MB'


def pull_outbox():
    print color_term('<%s>' % dir_data, 'red')
    saps_fetched = set()
    for sap in os.listdir(dir_data):
        dir_sap = os.path.join(dir_data, sap)
        if os.path.isdir(dir_sap):
            for f in os.listdir(dir_sap):
                if re.search(args.file_type, f):
                    print color_term('• copy %s ...' % f),
                    execute_cmd("rsync -t %s %s" % (os.path.join(dir_sap, f), os.path.join(dir_output, f)))
                    saps_fetched.add(sap)
                    print color_term(get_size(os.path.join(dir_output, f)), 'grey'),
                    print color_term('OK!', 'green')
                else:
                    print color_term('*PASS* %s' % f, 'grey')
    print '------------------'
    print color_term('Fetched %d samples' % len(saps_fetched))


def pull_miseq():
    sap_ids = set()
    print color_term('• read sample ids from output ... '),
    for f in os.listdir(dir_output):
        if re.search('\.bam$', f):
            # handle sample id
            sap_id = handle_sap_id(f)
            sap_ids.add(sap_id)
    print color_term('OK!', 'green')

    match_triger = 0
    saps_fetched = set()

    if not args.dir_fastq:
        for d in os.listdir(dir_miseq):
            if re.match("%s_M\d{5}_\d{4}_0{9}-" % run_bn, d):
                match_triger = 1
                print color_term('<%s>' % d, 'red')
                dir_data = os.path.join(os.path.join(dir_miseq, d), sub_dir)
                break
    else:
        dir_data = args.dir_fastq

    for f in os.listdir(dir_data):
        if re.search(args.file_type, f):
            sap_id_f = handle_sap_id(f)
            if sap_id_f in sap_ids:
                print color_term('• copy %s ...' % f),
                execute_cmd("rsync -t %s %s" % (os.path.join(dir_data, f), os.path.join(dir_output, f)))
                saps_fetched.add(sap_id_f)
                print color_term(get_size(os.path.join(dir_output, f)), 'grey'),
                print color_term('OK!', 'green')

    if not match_triger:
        print color_term("No data on MiSeq with RUN: %s" % run_bn, 'red')
    print '------------------'
    print color_term('Fetched %d samples' % len(saps_fetched))


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='pullData', formatter_class=argparse.RawTextHelpFormatter,
                                     description="pull NGS data with fast and extraordinarily versatile file copying tool - rsync")
    subparsers = parser.add_subparsers(dest='subparser_name', help='pull data with different source')

    parser_a = subparsers.add_parser('miseq', help='from MiSeq')
    parser_a.add_argument('run_bn', type=str, help='Specify run batch No.')
    parser_a.add_argument('dir_output', type=str, help='Specify directory of output')
    parser_a.add_argument('-dm', '--dir_miseq', type=str, default='/Volumes/MiSeqOutput', help='Specify directory of MiSeq')
    parser_a.add_argument('-df', '--dir_fastq', type=str, help='Specify directory of FASTQ')
    parser_a.add_argument('-f', '--file_type', metavar='REGEX', type=str, default='\.fastq(?:\.gz)?$', help='Specify file type need to pull')
    parser_a.set_defaults(func=pull_miseq)

    parser_b = subparsers.add_parser('outbox', help='from outbox')
    parser_b.add_argument('dir_data', type=str, help='Specify directory of data in outbox')
    parser_b.add_argument('dir_output', type=str, help='Specify directory of output')
    parser_b.add_argument('-f', '--file_type', metavar='REGEX', type=str, default='\.(?:ba[im]|vcf|txt)$', help='Specify file type need to pull')
    parser_b.set_defaults(func=pull_outbox)

    args = parser.parse_args()

    if args.subparser_name == 'miseq':
        run_bn = args.run_bn
        dir_output = args.dir_output
        dir_miseq = args.dir_miseq
        sub_dir = 'Data/Intensities/BaseCalls'
    elif args.subparser_name == 'outbox':
        dir_data = args.dir_data
        dir_output = args.dir_output

    args.func()
