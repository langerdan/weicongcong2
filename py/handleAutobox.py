#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : handleAutobox
# AUTHOR  : codeunsolved@gmail.com
# CREATED : December 20 2016
# VERSION : v0.0.1a
# ToDo:
# 1. class FileHandlerFormatter can ONLY format '%(message)s';
#    [Solved] with `return logging.Formatter.format(self, record)`,
#    1.1 but it affect on global, with StreamHandler too.
# 2. not real time output with subprocess(execute_cmd);

import os
import re
import sys
import time
import logging
import argparse
from argparse import RawTextHelpFormatter

from lib.base import SetupLogger
from lib.base import execute_cmd
from lib.base import print_colors
from lib.base import handle_project


def main():
    print "========================================================"
    print time.strftime("%Y年%m月%d日 %A %H:%M:%S", time.gmtime())
    print "========================================================"

    START = time.time()

    print print_colors("=>Project : ", 'green') + project
    print print_colors("=>RUN     : ", 'green') + run_bn
    print "--------------------------------------------------------"
    print print_colors("=>Data    : ", 'green') + dir_data
    print print_colors("=>Output  : ", 'green') + dir_output
    print print_colors("=>bed     : ", 'green') + path_bed
    print print_colors("=>Options : ", 'green') + options
    print "========================================================"

    if re.search('pull', options):
        print print_colors("<< pullOutbox >>")
        PULL_OUTBOX = time.time()
        execute_cmd("python %s/py/pullData.py outbox %s %s -f '\.(?:ba[im]|vcf|txt)$'" % (dir_ngs_dashboard, dir_data, dir_output))
        print "--------------------------------------------------------"
        print "pullOutbox time: %ss" % round(time.time() - PULL_OUTBOX, 2)
        print "========================================================"

        print print_colors("<< pullMiSeq >>")
        PULL_MISEQ = time.time()

        if re.match('\d{6}$', run_bn):
            run_bn_mod = run_bn
        elif re.match('\d{6}-', run_bn):
            run_bn_mod = re.match('(\d{6})-', run_bn).group(1)
        else:
            raise Exception("[pullMiSeq] invalid RUN: %s" % run_bn)

        execute_cmd("python %s/py/pullData.py miseq %s %s" % (dir_ngs_dashboard, run_bn_mod, dir_output))
        print "--------------------------------------------------------"
        print "pullMiSeq time: %ss" % round(time.time() - PULL_MISEQ, 2)
        print "========================================================"

    if re.search('cross', options):
        print print_colors("<< crossSNP >>")
        CROSS_SNP = time.time()
        if project == "BRCA":
            print print_colors("Project: BRCA", 'yellow')
            execute_cmd("python %s/py/crossSNP.py autobox %s -ic -pi" % (dir_ngs_dashboard, dir_data))
        else:
            execute_cmd("python %s/py/crossSNP.py autobox %s -ick -p %s -r %s" % (dir_ngs_dashboard, dir_data, project, run_bn))
        print "--------------------------------------------------------"
        print "crossSNP time: %ss" % round(time.time() - CROSS_SNP, 2)
        print "========================================================"

    if re.search('miss', options):
        print print_colors("<< checkMissing >>")
        CHK_MISSING = time.time()
        execute_cmd("python %s/py/checkMissing.py autobox %s -p %s -r %s" % (dir_ngs_dashboard, dir_data, project, run_bn))
        print "--------------------------------------------------------"
        print "checkMissing time: %ss" % round(time.time() - CHK_MISSING, 2)
        print "========================================================"

    if re.search('qc', options):
        print print_colors("<< FASTQC • STATS • DEPTH >>")
        PREQC = time.time()
        execute_cmd("%s/Pipelines/preVariantCalling.sh fastqcstatdepth %s %s" % 
                    (dir_ngs_manual, dir_output, path_bed))
        print "--------------------------------------------------------"
        print "preQC time: %ss" % round(time.time() - PREQC, 2)
        print "========================================================"

        print print_colors("<< QC Report >>")
        QC = time.time()
        execute_cmd("python %s/py/QC_Reporter.py %s %s -p %s -r %s"% (dir_ngs_dashboard, dir_output, path_bed, project, run_bn))
        print "--------------------------------------------------------"
        print "QC time: %ss" % round(time.time() - QC, 2)
        print "========================================================"

    if re.search('fusion', options):
        print print_colors("<< FusionGene >>")
        FUSION = time.time()
        execute_cmd("python %s/Project/FusionGene/markFusionGene.py %s %s %s" % 
                    (dir_ngs_manual, dir_output, path_bed, path_fg_list))
        print "--------------------------------------------------------"
        print "markFusionGene time: %ss" % round(time.time() - FUSION, 2)
        print "========================================================"

    print "Total time: %ss" % round(time.time() - START, 2)
    print "========================================================"


class FileHandlerFormatter(logging.Formatter):
    def format(self, record):
        record.msg = re.sub('\\033\[[0-8;]+m', '', record.msg)
        return logging.Formatter.format(self, record)


class SetupLoggerMod(SetupLogger):
    def add_filehandler(self):
        if self.on_file:
            # handle log directory
            if self.path_log:
                dir_name = os.path.dirname(self.path_log)
                if not os.path.exists(dir_name):
                    print "[WARNING] directory of log doesn't exist, create it!"
                    os.makedirs(dir_name)

            file_handler = logging.FileHandler(self.path_log, mode=self.log_mode)
            file_handler.setFormatter(FileHandlerFormatter(self.format_fh, self.format_date))
            self.l.addHandler(file_handler)


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    --------------------------------------------------------
    Refer: [Redirect stdout and stderr to a logger in Python]
           (https://www.electricmonk.nl/log/2011/08/14/redirect-stdout-and-stderr-to-a-logger-in-python/)
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='handleAutobox', formatter_class=RawTextHelpFormatter,
                                     description="process analysis after Autobox pipeline.")

    parser.add_argument('dir_data', type=str, help='Specify directory of data')
    parser.add_argument('dir_output', type=str, help='Specify directory of output')
    parser.add_argument('bed', type=str, help='Specify path of bed')
    parser.add_argument('options', type=str, help="Specify analysis options\n"
                                                  "--------------------\n"
                                                  "supported key words:\n"
                                                  "--------------------\n"
                                                  "pull   : pull data from outbox (.bam, .bai, .vcf, .txt)\n"
                                                  "                   from MiSeq  (.fastq)\n"
                                                  "cross  : crossSNP\n"
                                                  "miss   : checkMissing\n"
                                                  "qc     : generate QC report on Topgen-Dashboard\n"
                                                  "fusion : fusion gene calling\n"
                                                  "toSAM  : BAM -> SAM\n"
                                                  "--------------------\n")
    parser.add_argument('-p', '--project', type=str, help='Specify Project')
    parser.add_argument('-r', '--run_bn', type=str, help='Specify RUN batch No.')
    parser.add_argument('-w', '--log_write', action='store_true', help="Change log file mode='w'")

    args = parser.parse_args()

    dir_ngs_dashboard = '/Users/codeunsolved/NGS/NGS-Dashboard'
    dir_ngs_manual = '/Users/codeunsolved/NGS/NGS-Manual'
    path_fg_list = '/Users/codeunsolved/Downloads/NGS-Data/bed/fusion_gene_listv1.2'

    dir_data = args.dir_data
    dir_data_name = os.path.basename(dir_data)
    dir_output = args.dir_output
    path_bed = args.bed
    options = args.options

    # handle Project
    if args.project:
        project = args.project
    else:
        project = handle_project(dir_data_name)
    # handle RUN batch No.
    if args.run_bn:
        run_bn = args.run_bn
    else:
        run_bn = re.match("%s(\d+)" % project, dir_data_name).group(1)
    # setup log
    if args.log_write:
        log_file_mode = 'w'
    else:
        log_file_mode = 'a'

    SetupLogger('log', os.path.join(dir_output, 'handleAutobox.log'), log_mode=log_file_mode,
                   format_sh='%(message)s', format_fh='[%(levelname)s] %(message)s')
    logger = logging.getLogger('log')

    sys.stdout = StreamToLogger(logger, logging.INFO)
    sys.stderr = StreamToLogger(logger, logging.ERROR)

    main()
