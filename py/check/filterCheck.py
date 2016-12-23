#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re


complement_bp = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', '*': '*', 'X': 'X'}

def extract_checkpos(path_raw, path_checkpos, path_unhandle):
    com_num = 0
    remain = []
    unhandle = []
    with open(path_raw, 'rb') as raw:
        for line in raw:
            if re.match('#', line):
                continue
            gene = re.match('(\S+)\t', line).group(1)
            acc_num = re.match('\S+\t(\S+)\t', line).group(1)
            hgvs = re.match('(?:\S+\t){3}(\S+)\t', line).group(1)
            strand = re.match('(?:\S+\t){4}(\S+)\t', line).group(1)
            chr_ = 'chr' + re.match('(?:\S+\t){5}(\d+):', line).group(1)
            pos_s = re.match('(?:\S+\t){5}\d+:(\d+)-', line).group(1)
            pos_e = re.match('(?:\S+\t){5}\d+:\d+-(\d+)', line).group(1)
            if re.match('\w\.\d+\w>\w', hgvs):
                ref = re.search('(\w)>', hgvs).group(1)
                alt = re.search('>(\w)', hgvs).group(1)
                if strand == '-':
                    ref = complement_bp[ref]
                    alt = complement_bp[alt]
                    com_num += 1
                remain.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (chr_, pos_s, pos_e, gene, acc_num, hgvs, strand, ref, alt))
            else:
                if re.search('\w>\w$', hgvs):
                    ref = re.search('(\w)>', hgvs).group(1)
                    alt = re.search('>(\w)', hgvs).group(1)
                elif re.search('del\w$', hgvs):
                    ref = re.search('del(\w)$', hgvs).group(1)
                    alt = '*'
                else:
                    ref = 'X'
                    alt = 'X'
                if strand == '-':
                    ref = complement_bp[ref]
                    alt = complement_bp[alt]
                unhandle.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (chr_, pos_s, pos_e, gene, acc_num, hgvs, strand, ref, alt))

    print "Remain: %d/%d Unhandle: %d" % (len(remain), len(remain) + len(unhandle), len(unhandle))
    print "Complemet number: %d" % com_num
    with open(path_checkpos, 'wb') as cp:
        for x in remain:
            cp.write(x)

    with open(path_unhandle, 'wb') as uh:
        for x in unhandle:
            uh.write(x)


def extract_single_point(path_unhandle, path_sp, path_unhandle_2):
    single_point = []
    unhandle_2 = []
    with open(path_unhandle, 'rb') as uh:
        for line in uh:
            if re.match('#', line):
                continue
            try:
                pos_s = re.match('(?:\S+\t){1}(\d+)', line).group(1)
                pos_e = re.match('(?:\S+\t){2}(\d+)', line).group(1)
            except Exception as e:
                raise Exception(line)
            if pos_s == pos_e:
                single_point.append(line)
            else:
                unhandle_2.append(line)

    print "Single Point: %d" % len(single_point)
    with open(path_sp, 'wb') as sp:
        for x in single_point:
            sp.write(x)
    print "Remain: %d" % len(unhandle_2)
    with open(path_unhandle_2, 'wb') as uh2:
        for x in unhandle_2:
            uh2.write(x)

if __name__ == '__main__':
    dir_ = '/Users/codeunsolved/NGS/Topgen-Dashboard/py'
    extract_checkpos(os.path.join(dir_, 'NGS_Cancer_HotSpot_2016.12.09'), os.path.join(dir_, 'check_pos'), os.path.join(dir_, 'unhandle'))
    #Remain: 2091/2855 Unhandle: 764
    #Complemet number: 1340
    extract_single_point(os.path.join(dir_, 'unhandle'), os.path.join(dir_, 'single_point'), os.path.join(dir_, 'unhandle_2'))
    #Single Point: 267
    #Remain: 497