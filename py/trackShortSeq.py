#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : trackShortSeq
# AUTHOR  : codeunsolved@gmail.com
# CREATED : February 4 2017
# VERSION : v0.0.1a

from __future__ import division
import os
import re
import gzip
import math
import random
import argparse

from lib.base import color_term
from lib.base import execute_cmd



def stats(options='showoutput', level=range(10, 150, 10)):
    def open_fastq():
        if re.search('\.gz$', args.fastq.lower()):
            with gzip.GzipFile(args.fastq, 'rb') as f:
                for l in f:
                    yield l
        elif re.search('\.fastq$', args.fastq.lower()):
            with open(args.fastq, 'rb') as f:
                for l in f:
                    yield l
        else:
            raise Exception("Unknown file type: %s" % args.fastq)

    def output_s():
        with open(rl_path, 'wb') as o_s:
            o_s.write("%s\t%s\n" % ("Total", total))
            for k, v in distri_len_sorted:
                o_s.write("%s\t%s\n" % (k, v))

    distri_len = {}
    total = 0

    distri_len_level = dict(map(lambda x: (x, 0), level))
    step = level[1] - level[0]

    if args.subparser_name == 'track':
        short_seq = dict(map(lambda x: (x, []), level))
        range_start = int(args.sampling_range.split(',')[0])
        range_end = int(args.sampling_range.split(',')[1])
        sampling_seq = {}

    for i, line in enumerate(open_fastq()):
        line = line.strip()
        if i % 4 == 0:
            qname = line
        elif i % 4 == 1:
            if len(line) not in distri_len:
                distri_len[len(line)] = 1
            else:
                distri_len[len(line)] += 1
                if args.subparser_name == 'track':
                    if range_start <= len(line) < range_end:
                        for l in distri_len_level:
                            if l <= len(line) < l + step:
                                short_seq[l].append({"qname": qname, "seq": line, "len": len(line)})
            total += 1

    distri_len_sorted = sorted(distri_len.iteritems(), key=lambda d: d[0])
    for k, v in distri_len_sorted:
        for l in distri_len_level:
            if l <= k < l + step:
                distri_len_level[l] += v
                break

    if re.search('show', options):
        distri_len_level_sorted = sorted(distri_len_level.iteritems(), key=lambda d: d[0])
        print '\t'.join(["Total"] + [str(x[0]) for x in distri_len_level_sorted])
        print '\t'.join([str(total)] + [str(x[1]) for x in distri_len_level_sorted])

    if re.search('output', options):
        fastq_dir = os.path.dirname(args.fastq)
        fastq_fn = re.match('(.+)\.fastq(:?\.gz)$', os.path.basename(args.fastq), re.I).group(1)
        rl_path = os.path.join(fastq_dir, "%s.rl" % fastq_fn)
        print color_term("• output stats of reads length ..."),
        output_s()
        print color_term("OK!", 'green')

    if args.subparser_name == 'track':
        for l in short_seq:
            if len(short_seq[l]) == 0:
                continue
            elif len(short_seq[l]) < args.sampling_freq**-1:
                sampling_seq[l] = (random.sample(short_seq[l], 1))
            else:
                sampling_seq[l] = (random.sample(short_seq[l], int(math.ceil(len(short_seq[l]) * args.sampling_freq))))
        return sampling_seq


def track():
    def output_fasta():
        with open(fasta_path, 'wb') as fa:
            for l in s_seq_sorted:
                for s in l[1]:
                    if not re.search('N', s["seq"]):
                        fa.write(">[%s]-%s\n" % (l[0], s["qname"]))
                        fa.write("%s\n\n" % s["seq"])

    def stats_bls():
        query_seq = []
        with open(bls_path, 'rb') as bls:
            for line in bls:
                line = line.strip()
                if re.match("# Query:", line):
                    qname = re.match("# Query: (.+)$", line).group(1)
                    query_seq.append({"qname": qname, "match": []})
                elif re.match("#", line):
                    continue
                else:
                    bls_content = line.split('\t')
                    if bls_content[2] == '100.000':
                        query_seq[-1]["match"].append(bls_content[1])
        print '------------------'
        print color_term("Total Query: %d" % len(query_seq))
        nt_match = 0
        for q in query_seq:
            if len(q["match"]) > 0:
                nt_match += 1
        print color_term("nt 100%% match: %d/%d - %s%%" % (nt_match, len(query_seq), round(nt_match / len(query_seq) * 100, 2)))

    fastq_dir = os.path.dirname(args.fastq)
    fastq_fn = re.match('(.+)\.fastq(:?\.gz)$', os.path.basename(args.fastq), re.I).group(1)
    fasta_path = os.path.join(fastq_dir, '%s.ss_sampling.fa' % fastq_fn)
    bls_path = os.path.join(fastq_dir, '%s.ss_sampling.bls' % fastq_fn)

    if re.search('fa', args.options):
        s_range = range(*[int(x) for x in args.sampling_range.split(',')])
        s_seq_sorted = sorted(stats(options='show', level=s_range).iteritems(), key=lambda d: d[0])
        print color_term("output fasta..."),
        output_fasta()
        print color_term("OK!", 'green')

    if re.search('blast', args.options):
        print color_term("BLASTn with nt...")
        execute_cmd("blastn -query %s -db nt -outfmt 7 -out %s" % (fasta_path, bls_path))
        print color_term("OK!", 'green')

    if re.search('stats', args.options):
        stats_bls()

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='trackShortSeq', formatter_class=argparse.RawTextHelpFormatter,
                                     description="• stats sequence length distribution.\n"
                                                 "• track short sequence's source by random sampling.")
    subparsers = parser.add_subparsers(dest='subparser_name', help='')

    parser_a = subparsers.add_parser('stats', help='stat sequence length distribution')
    parser_a.add_argument('fastq', type=str, help='Specify path of .fastq/.fastq.zip file')
    parser_a.set_defaults(func=stats)

    parser_b = subparsers.add_parser('track', help="track short sequence's source by random sampling")
    parser_b.add_argument('fastq', type=str, help='Specify path of .fastq/.fastq.zip file')
    parser_b.add_argument('-f', '--sampling_freq', type=float, default=float(1/10**4), help='Specify sampling frequency')
    parser_b.add_argument('-r', '--sampling_range', metavar='START,END,STEP', type=str, default='20,150,10', help='Specify sampling step')
    parser_b.add_argument('--options', type=str, default='fablaststats', help='Specify options')
    parser_b.set_defaults(func=track)

    args = parser.parse_args()
    args.func()
