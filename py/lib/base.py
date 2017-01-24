#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : base
# AUTHOR  : codeunsolved@gmail.com
# CREATED : August 10 2016
# VERSION : v0.0.1a

import os
import re
import sys
import time
import shutil
import logging
import shlex
import subprocess

from threading import Thread


def read_bed(path_b, r_type='dict'):
    bed_dict = {}
    bed_list = []
    with open(path_b, 'rb') as bed:
        for line in bed:
            if not re.match('chr[1-9XYM]+\t', line):
                continue
            line_cont = line.strip().split('\t')
            chr_n = line_cont[0]
            pos_s = int(line_cont[1])
            pos_e = int(line_cont[2])
            if len(line_cont) >3:
                gene_name = line_cont[3]
            else:
                gene_name = "*"
            bed_dict["%s-%s-%s-%s" % (chr_n, gene_name, pos_s, pos_e)] = {"chr": chr_n, "start": pos_s, "end": pos_e, "gene": gene_name}
            bed_list.append({"chr": chr_n, "start": pos_s, "end": pos_e, "gene": gene_name})
    if r_type == 'dict':
        return bed_dict
    elif r_type == 'list':
        return bed_list
    else:
        raise Exception("Unknown return type: %s" % r_type)


def parse_vcf(p_vcf):
    vcf_body = []
    with open(p_vcf, 'rb') as vcf:
        ver = None
        for line_no, line in enumerate(vcf):
            if line_no == 0:
                ver = re.match('##fileformat=VCFv(.+)[\r\n]', line).group(1)
            if re.match('#', line):
                continue
            if ver == "4.1" or "4.2":
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
        'grey': '\033[1;30m',
        'red': '\033[1;31m',
        'green': '\033[1;32m',
        'yellow': '\033[1;33m',
        'blue': '\033[1;34m',
        'megenta': '\033[1;35m',
        'cyan': '\033[1;36m',
        'white': '\033[1;37m',
        'bold': '\033[1m',
        'end': '\033[0m'
    }
    return colors[color] + string + colors['end']


def get_file_path(dir_main, suffix='faa', output_type='list', r_num=2, debug=True):
    def recurse_dir(dir_r, path_list, suffix_r, r_num_r):
        r_num_r -= 1
        content_list = os.listdir(dir_r)
        for content in content_list:
            path_content = os.path.join(dir_r, content)
            if os.path.isdir(path_content) and r_num_r:
                recurse_dir(path_content, path_list, suffix, r_num_r)
            elif re.search('\.%s$' % suffix_r, content):
                if debug:
                    print path_content
                path_list.append(path_content)
        return path_list

    path_file = recurse_dir(dir_main, [], suffix, r_num)
    if output_type == 'list':
        return path_file
    elif output_type == 'txt':
        return '\n'.join(path_file)


def handle_sap_id(file_name):
    if re.search('_S\d+', file_name):
        return re.match('(.+)_S\d+', file_name).group(1)
    elif re.search('autoBox', file_name):
        return re.match('(.+)_20\d{2}_\d{2}_\d{2}', file_name).group(1)
    else:
        print print_colors('unknown sample source', 'red')
        return re.search('(.+)\.', file_name).group(1)


def handle_project(dir_name):
    if re.search('56gene', dir_name):
        project = '56gene'
    elif re.search('42geneLung', dir_name):
        project = '42geneLung'
    elif re.search('14geneCRC', dir_name):
        project = '14geneCRC'
    elif re.search('9geneBreast', dir_name):
        project = '9geneBreast'
    elif re.search('6geneGIST', dir_name):
        project = '6geneGIST'
    elif re.search('6geneOvarian', dir_name):
        project = '6geneOvarian'
    elif re.search('151gene', dir_name):
        project = '151gene'
    elif re.search('50gene', dir_name):
        project = '50gene'
    elif re.search('BRCA', dir_name):
        project = 'BRCA'
    elif re.match('TEST', dir_name):
        project = 'TEST'
    else:
        raise Exception("Unknown project for %s" % dir_name)
    return project


def handle_run_bn(dir_name):
    if re.match('BRCA|onco', dir_name):
        run_bn = re.match('(?:BRCA|onco)(\d+)', dir_name).group(1)
    else:
        raise Exception("Unknown RUN batch No. for %s" % dir_name)
    return run_bn


def handle_table(project):
    table = {'vcf': None, 'anno': None}
    if project in ['56gene', '42geneLung', '14geneCRC', '9geneBreast', '6geneGIST', '6geneOvarian', 
                   '151gene', '50gene', 'BRCA', 'ZS-BRCA', 'TEST']:
        table['vcf'] = project + '_VCF'
        table['anno'] = project + '_anno'
    else:
        raise Exception('Unknown Project: %s' % project)
    return table


def execute_cmd(c):
    p = subprocess.Popen(shlex.split(c), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    p.wait()
    if err:
        raise Exception(err)
    elif out:
        print out


class SetupLogger(object):
    def __init__(self, log_name, path_log=None, level=logging.DEBUG, on_file=True, on_stream=True, log_mode='a',
                 format_fh='%(asctime)s | %(filename)s - line:%(lineno)-4d | %(levelname)s | %(message)s',
                 format_sh='[%(levelname)s] %(message)s',
                 format_date='[%b-%d-%Y] %H:%M:%S'):
        self.log_name = log_name
        self.path_log = path_log
        self.level = level
        self.on_file = on_file
        self.on_stream = on_stream
        self.log_mode = log_mode
        self.format_fh = format_fh
        self.format_sh = format_sh
        self.format_date = format_date
        self.l = logging.getLogger(log_name)
        self.l.setLevel(level)
        self.add_filehandler()
        self.add_streamhandler()

    def add_filehandler(self):
        if self.on_file:
            # handle log directory
            if self.path_log:
                dir_name = os.path.dirname(self.path_log)
                if not os.path.exists(dir_name):
                    print "[WARNING] directory of log doesn't exist, create it!"
                    os.makedirs(dir_name)

            file_handler = logging.FileHandler(self.path_log, mode=self.log_mode)
            file_handler.setFormatter(logging.Formatter(self.format_fh, self.format_date))
            self.l.addHandler(file_handler)

    def add_streamhandler(self):
        if self.on_stream:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter(self.format_sh))
            self.l.addHandler(stream_handler)
