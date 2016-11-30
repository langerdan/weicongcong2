#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : pullMiSeq
# AUTHOR  : codeunsolved@gmail.com
# CREATED : November 21 2016
# VERSION : v0.0.1a

from __future__ import division
import os
import re
import shutil
import argparse
from argparse import RawTextHelpFormatter

from base import print_colors
from base import handle_sap_id
from database_connector import MysqlConnector


def get_size(path_file):
    file_size = os.path.getsize(path_file)
    return str(round(file_size / 1024 / 1024, 2)) + 'MB'

def main():
    sap_ids = set()
    print print_colors('• read sample ids from output ... '),
    for f in os.listdir(dir_output):
        if re.search('\.bam$', f):
            # handle sample id
            sap_id = handle_sap_id(f)
            sap_ids.add(sap_id)
    print print_colors('OK!', 'green')

    for d in os.listdir(dir_miseq):
        if re.match(run_bn, d):
            print print_colors('<%s>' % d, 'red')
            dir_data = os.path.join(os.path.join(dir_miseq, d), sub_dir)
            for f in os.listdir(dir_data):
                if re.search(args.file_type, f):
                    sap_id_f = handle_sap_id(f)
                    if sap_id_f in sap_ids:
                        print print_colors('• copy %s ...' % f),
                        shutil.copyfile(os.path.join(dir_data, f), os.path.join(dir_output, f))
                        print print_colors(get_size(os.path.join(dir_output, f)), 'grey'),
                        print print_colors('OK!', 'green')
    print '------------------'
    print print_colors('Fetched %d samples' % len(sap_ids))

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='pullMiSeq', formatter_class=RawTextHelpFormatter,
                                     description="Pull data from MiSeq")

    parser.add_argument('run_bn', type=str, help='Specify run batch No.')
    parser.add_argument('dir_output', type=str, help='Specify directory of output')
    parser.add_argument('-d', '--dir_miseq', type=str, help='Specify directory of MiSeq')
    parser.add_argument('-f', '--file_type', metavar='REGEX', type=str, default='\.fastq(?:\.gz)?$', help='Specify file type need to pull')

    args = parser.parse_args()

    run_bn = args.run_bn
    dir_output = args.dir_output
    dir_miseq = '/Volumes/MiSeqOutput'
    sub_dir = 'Data/Intensities/BaseCalls'
    if args.dir_miseq is not None:
        dir_miseq = args.dir_miseq

    main()
