#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : BASE_v0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : August 10 2016

import os
import re
import shutil


def read_bed(path_b):
    a_details = {}
    with open(path_b, 'rb') as r_obj_b:
        for line_no, line_b in enumerate(r_obj_b):
            if line_no > 0:
                chr_n = re.match('([^\t]+)\t', line_b).group(1)
                pos_s = int(re.match('[^\t]+\t([^\t]+\t)', line_b).group(1))
                pos_e = int(re.match('(?:[^\t]+\t){2}([^\t]+\t)', line_b).group(1))
                gene_name = re.match('(?:[^\t]+\t){3}([^\t\n\r]+)', line_b).group(1)
                if re.search('[:\-_]', gene_name):
                    gene_name = ' '
                a_details["%s-%s-%s" % (chr_n, gene_name, pos_s)] = [chr_n, pos_s, pos_e, gene_name]
    return a_details


def clean_output(dir_o, subdir_name):
    if os.path.isdir(os.path.join(dir_o, subdir_name)):
        shutil.rmtree(os.path.join(dir_o, subdir_name))
    os.mkdir(os.path.join(dir_o, subdir_name))
