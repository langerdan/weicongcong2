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
        for line_b in r_obj_b:
            chr_n = re.match('([^\t]+)\t', line_b).group(1)
            pos_s = int(re.match('[^\t]+\t([^\t]+\t)', line_b).group(1))
            pos_e = int(re.match('(?:[^\t]+\t){2}([^\t]+\t)', line_b).group(1))
            gene_name = re.match('(?:[^\t]+\t){3}([^\t\n\r]+)', line_b).group(1)
            a_details["%s-%s-%s" % (chr_n, gene_name, pos_s)] = [chr_n, pos_s, pos_e, gene_name]
    return a_details


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


def clean_output(dir_o, subdir_name):
    if os.path.isdir(dir_o):
        if os.path.isdir(os.path.join(dir_o, subdir_name)):
            shutil.rmtree(os.path.join(dir_o, subdir_name))
        os.mkdir(os.path.join(dir_o, subdir_name))
    else:
        os.makedirs(os.path.join(dir_o, subdir_name))
