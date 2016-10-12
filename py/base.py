#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : base
# AUTHOR  : codeunsolved@gmail.com
# CREATED : August 10 2016
# VERSION : v0.0.1a

import os
import re
import shutil


def read_bed(path_b):
    f_details = {}
    with open(path_b, 'rb') as bed:
        for line_b in bed:
            chr_n = re.match('([^\t]+)\t', line_b).group(1)
            pos_s = int(re.match('[^\t]+\t([^\t]+\t)', line_b).group(1))
            pos_e = int(re.match('(?:[^\t]+\t){2}([^\t]+\t)', line_b).group(1))
            gene_name = re.match('(?:[^\t]+\t){3}([^\t\n\r]+)', line_b).group(1)
            f_details["%s-%s-%s-%s" % (chr_n, gene_name, pos_s, pos_e)] = [chr_n, gene_name, pos_s, pos_e]
    return f_details


def parse_vcf(p_vcf):
    vcf_body = []
    with open(p_vcf, 'rb') as vcf:
        ver = None
        for line_no, line in enumerate(vcf):
            if line_no == 0:
                ver = re.match('##fileformat=VCFv(.+)[\r\n]', line).group(1)
            if re.match('#', line):
                continue
            if ver == "4.1":
                chr_n = re.match('([^\t]+)\t', line).group(1)
                pos = int(re.match('[^\t]+\t([^\t]+)\t', line).group(1))
                id_snp = re.match('(?:[^\t]+\t){2}([^\t]+)\t', line).group(1)
                ref = re.match('(?:[^\t]+\t){3}([^\t]+)\t', line).group(1)
                alt = re.match('(?:[^\t]+\t){4}([^\t]+)\t', line).group(1)
                qual = re.match('(?:[^\t]+\t){5}([^\t]+)\t', line).group(1)
                q_filter = re.match('(?:[^\t]+\t){6}([^\t]+)\t', line).group(1)
                info = re.match('(?:[^\t]+\t){7}([^\t]+)\t', line).group(1)
                format_key = re.match('(?:[^\t]+\t){8}([^\t]+)\t', line).group(1)
                format_value = re.match('(?:[^\t]+\t){9}([^\t\n\r]+)', line).group(1)
                vcf_body.append([chr_n, pos, id_snp, ref, alt, qual, q_filter, info, format_key, format_value])
    return vcf_body


def clean_output(dir_o, subdir_name):
    if os.path.isdir(dir_o):
        if os.path.isdir(os.path.join(dir_o, subdir_name)):
            shutil.rmtree(os.path.join(dir_o, subdir_name))
        os.mkdir(os.path.join(dir_o, subdir_name))
    else:
        os.makedirs(os.path.join(dir_o, subdir_name))


def print_colors(string, color='blue'):
    colors = {
        'red': '\033[1;31m',
        'green': '\033[1;32m',
        'yellow': '\033[1;33m',
        'blue': '\033[1;36m',
        'grey': '\033[1;30m',
        'bold': '\033[1m',
        'end': '\033[0m'
    }
    return colors[color] + string + colors['end']


def get_file_path(dir_main, suffix='faa', output_type='list', r_num=2):
    def recurse_dir(dir_r, path_list, suffix_r, r_num_r):
        r_num_r -= 1
        content_list = os.listdir(dir_r)
        for content in content_list:
            path_content = os.path.join(dir_r, content)
            if os.path.isdir(path_content) and r_num_r:
                recurse_dir(path_content, path_list, suffix, r_num_r)
            elif re.search('\.' + suffix_r + '$', content):
                print path_content
                path_list.append(path_content)
        return path_list

    path_file = recurse_dir(dir_main, [], suffix, r_num)
    if output_type == 'list':
        return path_file
    elif output_type == 'txt':
        return '\n'.join(path_file)
