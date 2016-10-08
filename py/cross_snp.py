#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : cross_SNP
# AUTHOR  : codeunsolved@gmail.com
# CREATED : September 20 2016
# VERSION : v0.0.1a

from __future__ import division
import os
import re
import sys
import xlwt

from base import parse_vcf
from database_connector import MysqlConnector
from config import mysql_config

# CONFIG AREA #
run_bn = int(sys.argv[1])
offset = int(sys.argv[2])
options = "importcross" if len(sys.argv) < 4 else sys.argv[3]

dir_prefix = "56gene20" + str(run_bn + offset)
dir_outbox = r'/Users/codeunsolved/TopgenData1/outbox'
vcf_col = ["Pipeline", "SAP_id", "RUN_bn", "Chr", "Pos", "RS_id", "Ref", "Alt", "Qual", "Filter", "Info", "Format",
           "Format_val", "AC", "AF", "AN", "DB", "DP", "FS", "MLEAC", "MLEAF", "MQ", "MQ0", "QD", "SOR",
           "BaseQRankSum", "MQRankSum", "ReadPosRankSum", "GT", "AD", "GQ", "PL"]
anno_col = ["Pipeline", "SAP_id", "RUN_bn", "Chr", "Pos_s", "Pos_e", "Ref", "Alt", "Func_refGene", "Gene_refGene",
            "ExonicFunc_refGene", "AAChange_refGene", "phastConsElements46way", "genomicSuperDups", "esp6500si_all",
            "1000g2014sep_all", "snp138", "ljb26_all", "cg69", "cosmic70", "clinvar_20140929", "Otherinfo1",
            "Otherinfo2", "Otherinfo3"]
onco_snp = [["chr1", 20915701, 20915701, "A", "C", "exonic", "CDA"],
            ["chr1", 97981395, 97981395, "T", "C", "exonic", "DPYD"],
            ["chr1", 98348885, 98348885, "G", "A", "exonic", "DPYD"],
            ["chr1", 11856378, 11856378, "G", "A", "exonic", "MTHFR"],
            ["chr1", 11854476, 11854476, "T", "G", "exonic", "MTHFR"],
            ["chr1", 97915614, 97915614, "G", "A", "", "DYPD*2A"],
            ["chr10", 101563815, 101563815, "G", "A", "exonic", "ABCC2(MRP2)"],
            ["chr10", 96741053, 96741053, "A", "C", "exonic", "CYP2C9"],
            ["chr11", 103418158, 103418158, "A", "G", "intergenic", "DYNC2H1(dist=67567),MIR4693(dist=302476)"],
            ["chr11", 67352689, 67352689, "A", "G", "exonic", "GSTP1"],
            ["chr11", 4159457, 4159457, "A", "G", "exonic", "RRM1"],
            ["chr11", 4159466, 4159466, "G", "A", "exonic", "RRM1"],
            ["chr18", 657646, 657673, "CCGCGCCACTTGGCCTGCCTCCGTCCCG", "-", "UTR5", "TYMS"],
            ["chr19", 41512841, 41512841, "G", "T", "exonic", "CYP2B6"],
            ["chr19", 41515263, 41515263, "A", "G", "exonic", "CYP2B6"],
            ["chr19", 45923653, 45923653, "A", "G", "exonic", "ERCC1"],
            ["chr19", 45867259, 45867259, "C", "T", "exonic", "ERCC2"],
            ["chr19", 45854919, 45854919, "T", "G", "exonic", "ERCC2"],
            ["chr19", 44055726, 44055726, "T", "C", "exonic", "XRCC1"],
            ["chr19", 44057574, 44057574, "G", "A", "exonic", "XRCC1"],
            ["chr2", 234669144, 234669144, "G", "A", "exonic", "UGT1A1"],
            ["chr2", 234668879, 234668879, "-", "AT", "intronic", "UGT1A10,UGT1A3,UGT1A4,UGT1A5,UGT1A6,UGT1A7,UGT1A8,UGT1A9"],
            ["chr22", 42526694, 42526694, "G", "A", "exonic", "CYP2D6"],
            ["chr3", 14187449, 14187449, "G", "T", "exonic", "XPC"],
            ["chr6", 160113872, 160113872, "A", "G", "exonic", "SOD2(MnSOD)"],
            ["chr6", 18130918, 18130918, "T", "C", "exonic", "TPMT"],
            ["chr7", 87138645, 87138645, "A", "G", "exonic", "ABCB1"]]
mismatch_offset = {0: 'red', -1: 'blue'}


def parse_info(info_txt):
    info = {}
    info_split = []
    for x in info_txt.split(';'):
        if re.search('=', x):
            info_key = re.match('(.+)=', x).group(1)
            info_val = re.search('=(.+)', x).group(1)
        else:
            info_key = x
            info_val = 'True'
        info[info_key] = info_val
    for i_k in vcf_col[13:28]:
        if i_k not in info:
            info_split.append('None')
        else:
            info_split.append(info[i_k])
    return info_split


def parse_format(format_keys, format_vals):
    format_split = []
    format_dict = dict(zip(format_keys.split(':'), format_vals.split(':')))
    for f_k in vcf_col[-4:]:
        if f_k not in format_dict:
            format_split.append('None')
        else:
            format_split.append(format_dict[f_k])
    return format_split


def import_vcf(data):
    insert_g = ("INSERT INTO 56gene_VCF "
                "(Pipeline, SAP_id, RUN_bn, Chr, Pos, RS_id, Ref, Alt, Qual, Filter, Info, Format, Format_val, "
                "AC, AF, AN, DB, DP, FS, MLEAC, MLEAF, MQ, MQ0, QD, SOR, BaseQRankSum, MQRankSum, ReadPosRankSum, "
                "GT, AD, GQ, PL) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                "%s, %s, %s, %s, %s, %s, %s, %s)")
    for d in data:
        if m_con.query("SELECT id FROM 56gene_VCF "
                       "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos=%s",
                       d[:5]).rowcount == 1:
            #print "=>record existed!\n=>update %s" % d[5:]
            m_con.query("UPDATE 56gene_VCF "
                        "SET RS_id=%s, Ref=%s, Alt=%s, Qual=%s, Filter=%s, Info=%s, Format=%s, "
                        "Format_val=%s, AC=%s, AF=%s, AN=%s, DB=%s, DP=%s, FS=%s, MLEAC=%s, MLEAF=%s, MQ=%s, MQ0=%s, "
                        "QD=%s, SOR=%s, BaseQRankSum=%s, MQRankSum=%s, ReadPosRankSum=%s, GT=%s, AD=%s, GQ=%s, PL=%s "
                        "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos=%s",
                        (d[5:] + d[:5]))
            m_con.cnx.commit()
        else:
            #print "=>insert %s" % d
            m_con.insert(insert_g, d)


def parse_anno(path_anno):
    anno_data = []
    with open(path_anno, 'rb') as r_obj:
        for line_no, line in enumerate(r_obj):
            if line_no == 0:
                continue
            anno_data.append(line.strip().split('\t'))
    return anno_data


def import_anno(data):
    insert_g = ("INSERT INTO 56gene_anno "
                "(Pipeline, SAP_id, RUN_bn, Chr, Pos_s, Pos_e, Ref, Alt, Func_refGene, Gene_refGene, ExonicFunc_refGene,"
                " AAChange_refGene, phastConsElements46way, genomicSuperDups, esp6500si_all, 1000g2014sep_all, snp138, "
                "ljb26_all, cg69, cosmic70, clinvar_20140929, Otherinfo1, Otherinfo2, Otherinfo3) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                "%s)")
    for d in data:
        if m_con.query("SELECT id FROM 56gene_anno "
                       "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos_s=%s",
                       d[:5]).rowcount == 1:
            #print "=>record existed!\n=>update %s" % d[5:]
            m_con.query("UPDATE 56gene_anno "
                        "SET Pos_e=%s, Ref=%s, Alt=%s, "
                        "Func_refGene=%s, Gene_refGene=%s, ExonicFunc_refGene=%s, AAChange_refGene=%s, "
                        "phastConsElements46way=%s, genomicSuperDups=%s, esp6500si_all=%s, 1000g2014sep_all=%s, "
                        "snp138=%s, ljb26_all=%s, cg69=%s, cosmic70=%s, clinvar_20140929=%s, Otherinfo1=%s, "
                        "Otherinfo2=%s, Otherinfo3=%s "
                        "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos_s=%s",
                        (d[:5] + d[5:]))
            m_con.cnx.commit()
        else:
            #print "=>insert %s" % d
            m_con.insert(insert_g, d)


def query_vcf(term):
    query_g = ("SELECT Chr, Pos, RS_id, Ref, Alt, Qual, Filter, Info, Format, Format_val, AD FROM 56gene_VCF "
               "WHERE Pipeline=%s AND SAP_id=%s AND Chr=%s AND Pos=%s AND Ref=%s AND Alt=%s")
    return m_con.query(query_g, term)


def query_anno(term):
    query_g = ("SELECT * FROM 56gene_anno "
               "WHERE Pipeline=%s AND SAP_id=%s AND Chr=%s AND Pos_s=%s AND Pos_e=%s AND Ref=%s AND Alt=%s")
    return m_con.query(query_g, term)


def query_vcf_offset(term):
    query_g = ("SELECT Chr, Pos, RS_id, Ref, Alt, Qual, Filter, Info, Format, Format_val, AD FROM 56gene_VCF "
               "WHERE Pipeline=%s AND SAP_id=%s AND Chr=%s AND Pos=%s")
    return m_con.query(query_g, term)


def handle_mismatch(term):
    for m_o in mismatch_offset:
        cursor_mis = query_vcf_offset(term[:3] + [int(term[3]) + m_o])
        if cursor_mis.rowcount == 1:
            return [0, m_o, cursor_mis]
    return [1]


def get_allele_fre(ad):
    a_f = []
    ad_list = [int(x) for x in ad.split(",")]
    for a_d in ad_list[1:]:
        a_f.append(round(a_d/(a_d + ad_list[0]), 4))
    return ", ".join([str(x) for x in a_f])


def set_style(height=210, bold=False, background_color='aqua', font_color='black', name='Microsoft YaHei UI'):
        style = xlwt.XFStyle()
        # font
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.colour_index = xlwt.Style.colour_map[font_color]
        font.height = height
        style.font = font
        # background color
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map[background_color]
        style.pattern = pattern
        return style


def output_cross(cross_snp_d, cross_anvc_d):
    path_cross_anvc = os.path.join(dir_sap, "%s_SNPv0.1a.xls" % sap_id)

    workbook = xlwt.Workbook(style_compression=2)
    sheet1 = workbook.add_sheet(u'SNP', cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet(sap_id, cell_overwrite_ok=True)
    # sheet1 table header
    sheet1.write(0, 0, 'Chr', set_style(220, True, 'light_blue'))
    sheet1.write(0, 1, 'Start', set_style(220, True, 'light_blue'))
    sheet1.write(0, 2, 'End', set_style(220, True, 'light_blue'))
    sheet1.write(0, 3, 'Ref', set_style(220, True, 'light_blue'))
    sheet1.write(0, 4, 'Alt', set_style(220, True, 'light_blue'))
    sheet1.write(0, 5, 'Func', set_style(220, True, 'light_blue'))
    sheet1.write(0, 6, 'Gene', set_style(220, True, 'light_blue'))
    sheet1.write(0, 7, 'Func.refGene', set_style(220, True, 'light_green'))
    sheet1.write(0, 8, 'Gene.refGene', set_style(220, True, 'light_green'))
    sheet1.write(0, 9, 'ExonicFunc.refGene', set_style(220, True, 'light_green'))
    sheet1.write(0, 10, 'AAChange.refGene', set_style(220, True, 'light_green'))
    sheet1.write(0, 11, 'Otherinfo', set_style(220, True, 'light_green'))
    sheet1.write(0, 12, 'VCF.Format.val', set_style(220, True, 'light_orange'))
    sheet1.write(0, 13, 'VCF.Format', set_style(220, True, 'light_orange'))
    # sheet1 table content
    for line_i, line in enumerate(onco_snp):
        for snp_i, snp in enumerate(line):
            sheet1.write(line_i + 1, snp_i, snp)
        for cross_snp_i, cross_snp in enumerate(cross_snp_d[line_i]):
            if len(cross_snp_d[line_i]) == 8:
                if 4 < cross_snp_i < 7:
                    sheet1.write(line_i + 1, cross_snp_i + 7, cross_snp, set_style(200, False, 'aqua', mismatch_offset[cross_snp_d[line_i][-1]]))
                else:
                    sheet1.write(line_i + 1, cross_snp_i + 7, cross_snp)
            else:
                sheet1.write(line_i + 1, cross_snp_i + 7, cross_snp)
    # sheet2 table header
    for vcf_i, vcf in enumerate(vcf_col[3:13]):
        sheet2.write(0, vcf_i, vcf_col[3 + vcf_i], set_style(220, True, 'light_orange'))
    sheet2.write(0, 10, "Frequency", set_style(220, True, 'light_orange'))
    for anno_i, anno in enumerate(anno_col[3:]):
        sheet2.write(0, anno_i + 11, anno_col[3 + anno_i], set_style(220, True, 'light_green'))
    # sheet2 table content
    for line_i, line in enumerate(cross_anvc_d):
        for cross_anvc_i, cross_anvc in enumerate(line):
            if len(line) == 33:
                if cross_anvc_i < 11:
                    sheet2.write(line_i + 1, cross_anvc_i, cross_anvc, set_style(200, False, 'aqua', mismatch_offset[line[-1]]))
                elif 10 < cross_anvc_i < 33:
                    sheet2.write(line_i + 1, cross_anvc_i, cross_anvc)
            else:
                sheet2.write(line_i + 1, cross_anvc_i, cross_anvc)
    workbook.save(path_cross_anvc)


def output_sum_ca(data):
    path_sum_ca = os.path.join(dir_run, "SNP-Annotation_VCF.xls")
    workbook = xlwt.Workbook(style_compression=2)
    sheet1 = workbook.add_sheet(str(run_bn), cell_overwrite_ok=True)
    # sheet1 table header
    sheet1.write(0, 0, "Sample ID", set_style(220, True, 'light_blue'))
    sheet1.write(0, 1, "RUN", set_style(220, True, 'light_blue'))
    for vcf_i, vcf in enumerate(vcf_col[3:13]):
        sheet1.write(0, vcf_i + 2, vcf_col[3 + vcf_i], set_style(220, True, 'light_orange'))
    sheet1.write(0, 12, "Frequency", set_style(220, True, 'light_orange'))
    for anno_i, anno in enumerate(anno_col[3:]):
        sheet1.write(0, anno_i + 13, anno_col[3 + anno_i], set_style(220, True, 'light_green'))
    # sheet1 table content
    for line_i, line in enumerate(data):
        for cross_anvc_i, cross_anvc in enumerate(line):
            if len(line) == 35:
                if cross_anvc_i < 2:
                    sheet1.write(line_i + 1, cross_anvc_i, cross_anvc)
                elif 1 < cross_anvc_i < 13:
                    sheet1.write(line_i + 1, cross_anvc_i, cross_anvc, set_style(200, False, 'aqua', mismatch_offset[line[-1]]))
                elif 12 < cross_anvc_i < 35:
                    sheet1.write(line_i + 1, cross_anvc_i, cross_anvc)
            else:
                sheet1.write(line_i + 1, cross_anvc_i, cross_anvc)
    workbook.save(path_sum_ca)

if __name__ == '__main__':
    vcf_data = []
    anno_data = []
    m_con = MysqlConnector(mysql_config, 'TopgenNGS')
    for run in os.listdir(dir_outbox):
        if re.match(dir_prefix, run):
            print "<%s>" % run
            sum_cross_anvc = []
            dir_run = os.path.join(dir_outbox, run)
            for sap in os.listdir(dir_run):
                dir_sap = os.path.join(dir_run, sap)
                if os.path.isdir(dir_sap):
                    print "-{%s}" % sap
                    cross_anvc_data = []
                    sap_id = re.match('(.+?)[._]', sap).group(1)
                    output_trigger = 0 if re.search('import', options) else 3
                    vcf_mismatch = {}
                    for file in os.listdir(dir_sap):
                        pipeline = re.search('%s(_.+_)$' % str(run_bn + offset), run).group(1)
                        if re.search('import', options) and re.search('raw_variants\.vcf$', file):
                            vcf_body = parse_vcf(os.path.join(dir_sap, file))
                            for vcf_line in vcf_body:
                                vcf_data.append([pipeline, sap_id, run_bn] + vcf_line + parse_info(vcf_line[-3]) + \
                                      parse_format(vcf_line[-2], vcf_line[-1]))
                            print "import vcf...",
                            import_vcf(vcf_data)
                            output_trigger |= 1
                            print "OK!"

                        if re.search('hg19_multianno\.txt$', file):
                            anno_body = parse_anno(os.path.join(dir_sap, file))
                            for anno_line in anno_body:
                                anno_data.append([pipeline, sap_id, run_bn] + anno_line)
                                if re.search('cross', options):
                                    # filter Func.refGene == "intronic"
                                    if anno_line[5] == "intronic":
                                        continue
                                    # filter ExonicFunc.refGene == "synonymous SNV"
                                    if anno_line[7] == "synonymous SNV":
                                        continue
                                    # filter 1000g2014sep_all > 0.01
                                    if anno_line[12] != '' and float(anno_line[12]) > 0.01:
                                        continue
                                    cursor = query_vcf([pipeline, sap_id] + anno_line[:2] + anno_line[3:5])
                                    if cursor.rowcount != 1:
                                        mismatch_state = handle_mismatch([pipeline, sap_id] + anno_line[:2])
                                        if mismatch_state[0]:
                                            print "=CROSS= miss match [%s][%s] " % (anno_line[0], anno_line[1])
                                            print "=%s" % anno_line
                                            cross_anvc_data.append(['', '', '', '', '', '', '', '', '', '', ''] + anno_line)
                                        else:
                                            print "=CROSS= %s match [%s][%s]" % (mismatch_state[1], anno_line[0], anno_line[1])
                                            vcf_mismatch["%s-%s-%s-%s" % (anno_line[0], anno_line[1], anno_line[3], anno_line[4])] = mismatch_state[1]
                                            row_v = mismatch_state[2].fetchone()
                                            cross_anvc_data.append(list(row_v[:-1]) +
                                                [get_allele_fre(row_v[-1])] + anno_line + [mismatch_state[1]])
                                    else:
                                        row_v = cursor.fetchone()
                                        cross_anvc_data.append(list(row_v[:-1]) +
                                            [get_allele_fre(row_v[-1])] + anno_line)
                            output_trigger |= 4
                            if re.search('import', options):
                                print "import Annotation...",
                                import_anno(anno_data)
                                output_trigger |= 2
                                print "OK!"

                        if re.search('cross', options) and output_trigger == 7:
                            output_trigger = 0 if re.search('import', options) else 3
                            cross_snp_data = []
                            for each_snp in onco_snp:
                                cross_snp_data.append([])
                                anno_mismatch = 0

                                cursor_a = query_anno([pipeline, sap_id] + each_snp[:5])
                                if cursor_a.rowcount != 1:
                                    cross_snp_data[-1] += ["", "", "", "", ""]
                                    anno_mismatch = 1
                                else:
                                    row_a = cursor_a.fetchone()
                                    cross_snp_data[-1] += list(row_a[9:13]) + [row_a[-3]]

                                vcf_key = "%s-%s-%s-%s" % (each_snp[0], each_snp[1], each_snp[3], each_snp[4])
                                if vcf_key in vcf_mismatch:
                                    cursor_v = query_vcf_offset([pipeline, sap_id] + [each_snp[0], each_snp[1] + vcf_mismatch[vcf_key]])
                                else:
                                    cursor_v = query_vcf([pipeline, sap_id] + each_snp[:2] + each_snp[3:5])
                                if cursor_v.rowcount != 1:
                                    mismatch_state = handle_mismatch([pipeline, sap_id] + each_snp[:2])
                                    if mismatch_state[0]:
                                        if anno_mismatch == 1:
                                            print "\t=SNP-ALL= miss match - %s" % each_snp[:5]
                                        else:
                                            print "\t=SNP-VCF= miss match - %s" % each_snp[:5]
                                        cross_snp_data[-1] += ["", ""]
                                    else:
                                        row_v = mismatch_state[2].fetchone()
                                        cross_snp_data[-1] += [row_v[-2], row_v[-3], mismatch_state[1]]
                                else:
                                    row_v = cursor_v.fetchone()
                                    cross_snp_data[-1] += [row_v[-2], row_v[-3]]
                            print "output cross SNP xls...",
                            output_cross(cross_snp_data, cross_anvc_data)
                            print "OK!"

                            for each_ca_d in cross_anvc_data:
                                sum_cross_anvc.append([sap_id, run_bn] + each_ca_d)
            output_sum_ca(sum_cross_anvc)
    m_con.done()
