#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : base
# AUTHOR  : codeunsolved@gmail.com
# CREATED : August 10 2016
# VERSION : v0.0.1
# UPDATE  : [v0.0.1] February 13 2017
# 1. integrate some basic and useful functions;
# 2. modified the way of parsing .tsv file(re.match() -> split());
# 3. add StetupLogger(), execute_cmd();
# 4. print_colors() change name to 'color_term';

import os
import re
import sys
import time
import shlex
import shutil
import logging
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
                line_cont = line.strip().split('\t')
                chr_n = line_cont[0]
                pos = int(line_cont[1])
                id_snp = line_cont[2]
                ref = line_cont[3]
                alt = line_cont[4]
                qual = line_cont[5]
                q_filter = line_cont[6]
                info = line_cont[7]
                format_key = line_cont[8]
                format_value = line_cont[9]
                vcf_body.append([chr_n, pos, id_snp, ref, alt, qual, q_filter, info, format_key, format_value])
    return vcf_body


def clean_output(dir_o, subdir_name):
    if os.path.isdir(dir_o):
        if os.path.isdir(os.path.join(dir_o, subdir_name)):
            shutil.rmtree(os.path.join(dir_o, subdir_name))
        os.mkdir(os.path.join(dir_o, subdir_name))
    else:
        os.makedirs(os.path.join(dir_o, subdir_name))


def get_file_path(dir_main, suffix=None, output_type='list', r_num=2, debug=True):
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


def color_term(string, color='blue'):
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


class FileHandlerFormatter(logging.Formatter):
    def format(self, record):
        msg = super(FileHandlerFormatter, self).format(record)
        return re.sub('\\033\[[0-8;]+m', '', msg)


class SetupLogger(object):
    def __init__(self, log_name, path_log=None, level=logging.INFO, on_file=True, on_stream=True, log_mode='a',
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
            if self.path_log: # handle log directory
                dir_name = os.path.dirname(self.path_log)
                if not os.path.exists(dir_name):
                    print color_term("[WARNING] directory of log doesn't exist, create it!", 'yellow')
                    os.makedirs(dir_name)

            file_handler = logging.FileHandler(self.path_log, mode=self.log_mode)
            file_handler.setFormatter(FileHandlerFormatter(self.format_fh, self.format_date))
            self.l.addHandler(file_handler)

    def add_streamhandler(self):
        if self.on_stream:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter(self.format_sh))
            self.l.addHandler(stream_handler)


def execute_cmd(c):
    p = subprocess.Popen(shlex.split(c), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = p.stdout.readline()
        if output == '' and p.poll() is not None:
            break
        if output:
            print output.strip()

    error = p.stderr.read()
    if error:
        raise Exception(error)


# NGS
ngs_projects = ['56gene', '42geneLung', '14geneCRC', '9geneBreast', '6geneGIST', '6geneOvarian', 
                '151gene', '50gene', 'BRCA', 'ZS-BRCA', 'TEST']

def handle_project(dir_name):
    for p in ngs_projects:
        if re.search(p, dir_name):
            return p
    raise Exception("Unknown project for %s" % dir_name)


def handle_table(project):
    table = {'vcf': None, 'anno': None}
    if project in ngs_projects:
        table['vcf'] = project + '_VCF'
        table['anno'] = project + '_anno'
    else:
        raise Exception('Unknown Project: %s' % project)
    return table


def handle_run_bn(dir_name):
    if re.match('BRCA|onco', dir_name):
        run_bn = re.match('(?:BRCA|onco)(\d+)', dir_name).group(1)
    else:
        raise Exception("Unknown RUN batch No. for %s" % dir_name)
    return run_bn


def handle_sap_id(file_name):
    if re.search('_S\d+', file_name):
        return re.match('(.+)_S\d+', file_name).group(1)
    elif re.search('autoBox', file_name):
        return re.match('(.+)_20\d{2}_\d{2}_\d{2}', file_name).group(1)
    else:
        print color_term("Unknown sample source", 'red')
        return re.search('(.+)\.', file_name).group(1)
