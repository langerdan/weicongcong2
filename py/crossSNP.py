#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : crossSNP
# AUTHOR  : codeunsolved@gmail.com
# CREATED : September 20 2016
# VERSION : v0.0.3
# UPDATE  : [v0.0.1] October 12 2016
# 1. add argparse to parse args;
# 2. add three filter for annotation: 
#     i. Func.refGene == "intronic";
#     ii. ExonicFunc.refGene == "synonymous SNV";
#     iii. 1000g2014sep_all > 0.01;
# UPDATE  : [v0.0.2] November 20 2016
# 1. optimize subparsers{autobox, local} to handle Projec and more flexible directory name;
# 2. optimize query vcf/anno to handle multiple run on same sample, and add Exception for multiple match;
# UPDATE  : [v0.0.3] December 5 2016
# 1. [BugFix] fix inline if...else syntax in import_xxx status print;
# 2. add KnowledgeDB - MyCancerGenome match, -k, --add_knowledge;
# 3. fix offset table header;
# 4. add "No mutation after filter!" infomation for sample without mutation after filter;
# 5. add filter trigger for Func.refGene == "intronic";

from __future__ import division
import os
import re
import sys
import xlwt
import argparse
from argparse import RawTextHelpFormatter

from base import parse_vcf
from base import print_colors
from config import mysql_config
from database_connector import MysqlConnector

# CONFIG AREA #
vcf_col = ["Pipeline", "SAP_id", "RUN_bn", "Chr", "Pos", "RS_id", "Ref", "Alt", "Qual", "Filter", "Info", "Format",
           "Format_val", "AC", "AF", "AN", "DB", "DP", "FS", "MLEAC", "MLEAF", "MQ", "MQ0", "QD", "SOR",
           "BaseQRankSum", "MQRankSum", "ReadPosRankSum", "GT", "AD", "GQ", "PL"]
anno_col = ["Pipeline", "SAP_id", "RUN_bn", "Chr", "Pos_s", "Pos_e", "Ref", "Alt", "Func_refGene", "Gene_refGene",
            "ExonicFunc_refGene", "AAChange_refGene", "phastConsElements46way", "genomicSuperDups", "esp6500si_all",
            "1000g2014sep_all", "snp138", "ljb26_all", "cg69", "cosmic70", "clinvar_20140929", "Otherinfo1",
            "Otherinfo2", "Otherinfo3"]
knownledge_col = ["MyCancerGenome_disease", "MyCancerGenome_variant", "MyCancerGenome_freq", "MyCancerGenome_response"]

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
            ["chr7", 87138645, 87138645, "A", "G", "exonic", "ABCB1"],
            ["chr16", 69745145, 69745145, "C", "T", "exonic", "NQO1"],
            ["chr16", 69748869, 69748869, "C", "T", "exonic", "NQO1"],
            ["chr3", 124456742, 124456742, "G", "C", "exonic", "OPRT"],
            ["chr2", 95539307, 95539307, "A", "G", "exonic", "TEKT4"],
            ["chr2", 95539313, 95539313, "A", "G", "exonic", "TEKT4"]]
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


def parse_anno(path_anno):
    anno_data = []
    with open(path_anno, 'rb') as r_obj:
        for line_no, line in enumerate(r_obj):
            if line_no == 0:
                continue
            anno_data.append(line.strip().split('\t'))
    return anno_data


def import_vcf(data, table, is_update=True):
    insert_g = ("INSERT INTO {} "
                "(Pipeline, SAP_id, RUN_bn, Chr, Pos, RS_id, Ref, Alt, Qual, Filter, Info, Format, Format_val, "
                "AC, AF, AN, DB, DP, FS, MLEAC, MLEAF, MQ, MQ0, QD, SOR, BaseQRankSum, MQRankSum, ReadPosRankSum, "
                "GT, AD, GQ, PL) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(table))
    update = 0
    insert = 0
    ignore = 0
    for d in data:
        if m_con.query("SELECT id FROM {} "
                       "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos=%s".format(table),
                       d[:5]).rowcount == 1:
            if is_update:
                update += 1
                m_con.query("UPDATE {} "
                            "SET RS_id=%s, Ref=%s, Alt=%s, Qual=%s, Filter=%s, Info=%s, Format=%s, "
                            "Format_val=%s, AC=%s, AF=%s, AN=%s, DB=%s, DP=%s, FS=%s, MLEAC=%s, MLEAF=%s, MQ=%s, MQ0=%s, "
                            "QD=%s, SOR=%s, BaseQRankSum=%s, MQRankSum=%s, ReadPosRankSum=%s, GT=%s, AD=%s, GQ=%s, PL=%s "
                            "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos=%s".format(table),
                            (d[5:] + d[:5]))
                m_con.cnx.commit()
            else:
                ignore += 1
        else:
            insert += 1
            m_con.insert(insert_g, d)
    insert_s = "insert %s " % insert if insert else ""
    update_s = "update %s " % update if update else ""
    ignore_s = "ignore %s " % ignore if ignore else ""
    print print_colors(insert_s + update_s + ignore_s, 'grey'),


def import_anno(data, table, is_update=True):
    insert_g = ("INSERT INTO {} "
                "(Pipeline, SAP_id, RUN_bn, Chr, Pos_s, Pos_e, Ref, Alt, Func_refGene, Gene_refGene, ExonicFunc_refGene,"
                " AAChange_refGene, phastConsElements46way, genomicSuperDups, esp6500si_all, 1000g2014sep_all, snp138, "
                "ljb26_all, cg69, cosmic70, clinvar_20140929, Otherinfo1, Otherinfo2, Otherinfo3) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                "%s)".format(table))
    update = 0
    insert = 0
    ignore = 0
    for d in data:
        if m_con.query("SELECT id FROM {} "
                       "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos_s=%s".format(table),
                       d[:5]).rowcount == 1:
            if is_update:
                update += 1
                m_con.query("UPDATE {} "
                            "SET Pos_e=%s, Ref=%s, Alt=%s, "
                            "Func_refGene=%s, Gene_refGene=%s, ExonicFunc_refGene=%s, AAChange_refGene=%s, "
                            "phastConsElements46way=%s, genomicSuperDups=%s, esp6500si_all=%s, 1000g2014sep_all=%s, "
                            "snp138=%s, ljb26_all=%s, cg69=%s, cosmic70=%s, clinvar_20140929=%s, Otherinfo1=%s, "
                            "Otherinfo2=%s, Otherinfo3=%s "
                            "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos_s=%s".format(table),
                            (d[:5] + d[5:]))
                m_con.cnx.commit()
            else:
                ignore += 1
        else:
            insert += 1
            m_con.insert(insert_g, d)
    insert_s = "insert %s " % insert if insert else ""
    update_s = "update %s " % update if update else ""
    ignore_s = "ignore %s " % ignore if ignore else ""
    print print_colors(insert_s + update_s + ignore_s, 'grey'),


def query_vcf(term, table):
    query_g = ("SELECT Chr, Pos, RS_id, Ref, Alt, Qual, Filter, Info, Format, Format_val, AD FROM {} "
               "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos=%s AND Ref=%s AND Alt=%s".format(table))
    return m_con.query(query_g, term)


def query_anno(term, table):
    query_g = ("SELECT * FROM {} "
               "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos_s=%s AND Pos_e=%s AND Ref=%s AND Alt=%s".format(table))
    return m_con.query(query_g, term)


def query_vcf_offset(term, table):
    query_g = ("SELECT Chr, Pos, RS_id, Ref, Alt, Qual, Filter, Info, Format, Format_val, AD FROM {} "
               "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos=%s".format(table))
    return m_con.query(query_g, term)


def handle_mismatch(term):
    for m_o in mismatch_offset:
        cursor_mis = query_vcf_offset(term[:4] + [int(term[4]) + m_o], table_vcf)
        if cursor_mis.rowcount == 1:
            return [0, m_o, cursor_mis]
        elif cursor_mis.rowcount > 1:
            raise Exception('[CROSS_VAR][HANDLE_MIS]: %d match in VCF: %s' (cursor_mis.rowcount, str(term[:4] + [int(term[4]) + m_o])))
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


def output_cross(cross_snp_d, cross_anvc_d, dir_output, sap_id):
    path_cross_anvc = os.path.join(dir_output, "%s_SNP.xls" % sap_id)

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
    sheet1.write(0, 14, 'offset', set_style(220, True, 'light_orange'))
    # sheet1 table content
    for line_i, line in enumerate(onco_snp):
        for snp_i, snp in enumerate(line):
            sheet1.write(line_i + 1, snp_i, snp)
        for cross_snp_i, cross_snp in enumerate(cross_snp_d[line_i]):
            if cross_snp_d[line_i][7] in mismatch_offset:
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
    sheet2.write(0, 32, "offset", set_style(220, True, 'light_orange'))
    if args.add_knowledge:
        for k_i, k in enumerate(knownledge_col):
            sheet2.write(0, k_i + 33, k, set_style(220, True, 'light_turquoise'))

    # sheet2 table content
    for line_i, line in enumerate(cross_anvc_d):
        for cross_anvc_i, cross_anvc in enumerate(line):
            if line[32]:
                if cross_anvc_i < 11:
                    sheet2.write(line_i + 1, cross_anvc_i, cross_anvc, set_style(200, background_color='aqua',
                                                                                 font_color=mismatch_offset[line[32]]))
                else:
                    sheet2.write(line_i + 1, cross_anvc_i, cross_anvc)
            else:
                sheet2.write(line_i + 1, cross_anvc_i, cross_anvc)
    workbook.save(path_cross_anvc)


def output_sum_ca(data, dir_output, run_bn):
    path_sum_ca = os.path.join(dir_output, "SNP-Annotation_VCF.xls")
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
    sheet1.write(0, 34, "offset", set_style(220, True, 'light_orange'))
    if args.add_knowledge:
        for k_i, k in enumerate(knownledge_col):
            sheet1.write(0, k_i + 35, k, set_style(220, True, 'light_turquoise'))
    # sheet1 table content
    for line_i, line in enumerate(data):
        for cross_anvc_i, cross_anvc in enumerate(line):
            if len(line) != 3 and line[34] in mismatch_offset:
                if 1 < cross_anvc_i < 13:
                    sheet1.write(line_i + 1, cross_anvc_i, cross_anvc, set_style(200, background_color='aqua', font_color=mismatch_offset[line[34]]))
                else:
                    sheet1.write(line_i + 1, cross_anvc_i, cross_anvc)
            else:
                sheet1.write(line_i + 1, cross_anvc_i, cross_anvc)
    workbook.save(path_sum_ca)


def add_knowledge(data):
    def parse_hgvs(s):
        if s:
            g_h = set()
            vs = s.split(',')
            for v in vs:
                g = re.match('(\w+):', v).group(1)
                c = re.search(':([^:]+):[^:]+$', v).group(1)
                if not re.search("(?:ins|del)", c):
                    c_ref = re.match('\w\.(\w)', c).group(1)
                    c = re.sub('(?<=\d)(?=[AGTC])', '%s>' % c_ref, re.sub('(?<=^\w\.)%s' % c_ref, '', c))
                g_h.add((g, c))
                #print "from: %s, to: %s" % (v, c)
            return g_h
        else:
            return 0

    def query_mycansergenome(con, term):
        query_g = ("SELECT disease, variant, variant_table FROM MyCancerGenome_Variant "
                   "WHERE gene=%s AND variant_form=%s")
        return con.query(query_g, term)

    def get_response(s):
        response_html = re.findall('<td>(Response to.+?\n<td>.+?)<', s)
        return ' | '.join([re.sub('</td>\n<td>', '-', x) for x in response_html])

    def add_mycancergenome_data(result, data):
        variant_name = re.search('\((.+)\)', result[1]).group(1)
        freq = re.search('<td>Frequency of (?:<em>)?%s.+?</td>\n<td>(.+?)(?:\(|<)' % variant_name, result[2]).group(1)
        response = get_response(result[2])
        data[0].append(result[0])
        data[1].append(result[1])
        data[2].append(freq)
        data[3].append(response)
        print print_colors("Got MyCanserGenome item: %s" % [result[0], result[1], freq, response], 'green')

    m_con_k = MysqlConnector(mysql_config, 'KnowledgeDB')
    for i, d in enumerate(data):
        # add MyCanserGenome
        gene_hgvs = parse_hgvs(d[19])
        if gene_hgvs:
            if len(gene_hgvs) != 1:
                print print_colors("[ADD_KNOWLEDGE] got ONE more HGVS: %s-%s | %s" % (d[11], d[12], list(gene_hgvs)), 'yellow')
            d_mycancergenome = [[] for x in range(len(knownledge_col[:4]))]
            for g, h in gene_hgvs:
                cursor_mcg = query_mycansergenome(m_con_k, (g, h))
                if cursor_mcg.rowcount == 1:
                    r = cursor_mcg.fetchone()
                    add_mycancergenome_data(r, d_mycancergenome)
                elif cursor_mcg.rowcount == 0:
                    pass
                else:
                    #raise Exception('[ADD_KNOWLEDGE][MyCancerGenome]: %d match in MyCancerGenome_Variant: %s' % (cursor_mcg.rowcount, (g, h)))
                    print print_colors('[ADD_KNOWLEDGE][MyCancerGenome]: %d match in MyCancerGenome_Variant: %s' % (cursor_mcg.rowcount, (g, h)), 'yellow')
                    for r in cursor_mcg.fetchall():
                        add_mycancergenome_data(r, d_mycancergenome)
            d += [', '.join(x) for x in d_mycancergenome]
        else:
            d += ["", "", "", ""]
    m_con_k.done()


def cross_var(path_file, anno_data, cross_anvc_data, pipeline, sap_id, run_bn, vcf_mismatch):
    anno_body = parse_anno(path_file)
    for anno_line in anno_body:
        anno_data.append([pipeline, sap_id, run_bn] + anno_line)
        if args.cross:
            # filter Func.refGene == "intronic"
            if not args.pass_filter_intronic:
                if anno_line[5] == "intronic":
                    continue
            # filter ExonicFunc.refGene == "synonymous SNV"
            if anno_line[7] == "synonymous SNV":
                continue
            # filter 1000g2014sep_all > 0.01
            if anno_line[12] != '' and float(anno_line[12]) > 0.01:
                continue
            cursor = query_vcf([pipeline, sap_id, run_bn] + anno_line[:2] + anno_line[3:5], table_vcf)
            if cursor.rowcount == 0:
                mismatch_state = handle_mismatch([pipeline, sap_id, run_bn] + anno_line[:2])
                if mismatch_state[0]:
                    print print_colors("=CROSS= miss match [%s][%s] " % (anno_line[0], anno_line[1]), 'grey')
                    print print_colors("=%s" % anno_line, 'grey')
                    cross_anvc_data.append(['', '', '', '', '', '', '', '', '', '', ''] + anno_line)
                else:
                    print print_colors("=CROSS= %s match [%s][%s]" % (mismatch_state[1], anno_line[0], anno_line[1]), 'grey')
                    vcf_mismatch["%s-%s-%s-%s" % (anno_line[0], anno_line[1], anno_line[3], anno_line[4])] = mismatch_state[1]
                    row_v = mismatch_state[2].fetchone()
                    cross_anvc_data.append(list(row_v[:-1]) + [get_allele_fre(row_v[-1])] + anno_line + [mismatch_state[1]])
            elif cursor.rowcount == 1:
                row_v = cursor.fetchone()
                cross_anvc_data.append(list(row_v[:-1]) + [get_allele_fre(row_v[-1])] + anno_line + [""])
            else:
                raise Exception('[CROSS_VAR][QUERY_VCF]: %d match in VCF: %s' % (cursor.rowcount, str([pipeline, sap_id, run_bn] + anno_line[:2] + anno_line[3:5])))


def cross_snp(pipeline, sap_id, run_bn, vcf_mismatch):
    cross_snp_data = []
    for snp in onco_snp:
        cross_snp_data.append([])
        anno_mismatch = 0

        cursor_a = query_anno([pipeline, sap_id, run_bn] + snp[:5], table_anno)
        if cursor_a.rowcount == 0:
            cross_snp_data[-1] += ["", "", "", "", ""]
            anno_mismatch = 1
        elif cursor_a.rowcount == 1:
            row_a = cursor_a.fetchone()
            cross_snp_data[-1] += list(row_a[9:13]) + [row_a[-3]]
        else:
            raise Exception('[CROSS_SNP][QUERY_ANNO]: %d match in ANNO: %s' % (cursor_a.rowcount, str([pipeline, sap_id, run_bn] + snp[:5])))

        vcf_key = "%s-%s-%s-%s" % (snp[0], snp[1], snp[3], snp[4])
        if vcf_key in vcf_mismatch:
            cursor_v = query_vcf_offset([pipeline, sap_id, run_bn] + [snp[0], snp[1] + vcf_mismatch[vcf_key]], table_vcf)
        else:
            cursor_v = query_vcf([pipeline, sap_id, run_bn] + snp[:2] + snp[3:5], table_vcf)
        if cursor_v.rowcount == 0:
            mismatch_state = handle_mismatch([pipeline, sap_id, run_bn] + snp[:2])
            if mismatch_state[0]:
                if anno_mismatch == 1:
                    print print_colors("=SNP-ALL= miss match - %s" % snp[:5], 'grey')
                else:
                    print print_colors("=SNP-VCF= miss match - %s" % snp[:5], 'grey')
                cross_snp_data[-1] += ["", "", ""]
            else:
                row_v = mismatch_state[2].fetchone()
                cross_snp_data[-1] += [row_v[-2], row_v[-3], mismatch_state[1]]
        elif cursor_v.rowcount == 1:
            row_v = cursor_v.fetchone()
            cross_snp_data[-1] += [row_v[-2], row_v[-3], ""]
        else:
            raise Exception('[CROSS_SNP][QUERY_VCF]: %d match in VCF: %s' % (cursor_v.rowcount, str([pipeline, sap_id, run_bn] + snp[:2] + snp[3:5])))
    return cross_snp_data


def handle_autobox():
    project = args.project
    run_bn = args.run_bn
    offset = args.offset
    suffix = args.suffix

    dir_outbox = args.dir_outbox
    dir_prefix = project + str(run_bn + offset) + suffix + '_'

    for run in os.listdir(dir_outbox):
        if re.match(dir_prefix, run):
            print print_colors("<%s>" % run, 'red')
            pipeline = re.search('%s(_.+_?)$' % (str(run_bn + offset) + suffix), run).group(1) # need parenthesis to cover (str(run_bn + offset) + suffix)
            dir_run = os.path.join(dir_outbox, run)

            sum_cross_anvc = []
            for sap in os.listdir(dir_run):
                vcf_data = []
                anno_data = []

                dir_sap = os.path.join(dir_run, sap)
                if os.path.isdir(dir_sap):
                    print print_colors("-{%s}" % sap)
                    cross_anvc_data = []
                    sap_id = re.match('(.+?)[._]', sap).group(1)
                    output_trigger = 0 if args.import_var else 3
                    vcf_mismatch = {}
                    for f in os.listdir(dir_sap):
                        if args.import_var and re.search('raw_variants\.vcf$', f):
                            vcf_body = parse_vcf(os.path.join(dir_sap, f))
                            for vcf_line in vcf_body:
                                vcf_data.append([pipeline, sap_id, run_bn] + vcf_line + parse_info(vcf_line[-3]) + \
                                                parse_format(vcf_line[-2], vcf_line[-1]))
                            print "• import vcf ...",
                            import_vcf(vcf_data, table_vcf, is_update=args.update)
                            output_trigger |= 1
                            print print_colors("OK!", 'green')

                        if re.search('hg19_multianno\.txt$', f):
                            cross_var(os.path.join(dir_sap, f), anno_data, cross_anvc_data, pipeline, sap_id, run_bn, vcf_mismatch)
                            output_trigger |= 4
                            if args.import_var:
                                print "• import Annotation ...",
                                import_anno(anno_data, table_anno, is_update=args.update)
                                output_trigger |= 2
                                print print_colors("OK!", 'green')

                        if args.cross and output_trigger == 7:
                            output_trigger = 0 if args.cross else 3
                            cross_snp_data = cross_snp(pipeline, sap_id, run_bn, vcf_mismatch)
                            if args.add_knowledge:
                                add_knowledge(cross_anvc_data)
                            print "• output cross SNP xls ...",
                            output_cross(cross_snp_data, cross_anvc_data, dir_sap, sap_id)
                            print print_colors("OK!", 'green')

                            if cross_anvc_data:
                                for each in cross_anvc_data:
                                    sum_cross_anvc.append([sap_id, run_bn] + each)
                            else:
                                print print_colors("No mutation after filter!", 'yellow')
                                sum_cross_anvc.append([sap_id, run_bn, "No mutation after filter!"])
            output_sum_ca(sum_cross_anvc, dir_run, run_bn)


def handle_local():
    pipeline = args.pipeline
    run_bn = args.run_bn
    dir_data = args.dir_data

    print print_colors("<%s>" % dir_data, 'red')

    sap_ids = {}
    for f in os.listdir(dir_data):
        if args.import_var and re.search('\.vcf$', f):
            vcf_data = []

            # handle sample id
            if pipeline == 'Miseq':
                sap_id = re.match('(.+)_S\d+', f).group(1)
            else:
                sap_id = re.match('(.+)\.vcf', f).group(1)

            if sap_id not in sap_ids:
                print print_colors("-{%s}" % sap_id)
                sap_ids[sap_id] = 0

            vcf_body = parse_vcf(os.path.join(dir_data, f))
            for vcf_line in vcf_body:
                vcf_data.append([pipeline, sap_id, run_bn] + vcf_line + parse_info(vcf_line[-3]) + \
                                parse_format(vcf_line[-2], vcf_line[-1]))
            print "• import vcf ...",
            import_vcf(vcf_data, table_vcf, is_update=args.update)
            sap_ids[sap_id] |= 1
            print print_colors("OK!", 'green')


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='cross SNP', formatter_class=RawTextHelpFormatter,
                                     description="• import vcf, annotation(.vcf, raw_variants.txt)\n"
                                                 "• cross vcf with annotation and output report(.xls)")
    subparsers = parser.add_subparsers(help='cross snp with different source')

    parser_a = subparsers.add_parser('autobox', help='from autobox')
    parser_a.add_argument('project', type=str, help='Specify Project prefix')
    parser_a.add_argument('run_bn', type=int, help='Specify RUN batch No.')
    parser_a.add_argument('--offset', type=int, default=0, help='Specify day offset')
    parser_a.add_argument('--suffix', type=str, default='', help='Specify directory suffix')
    parser_a.add_argument('-d', '--dir_outbox', type=str, default='/Users/codeunsolved/TopgenData1/outbox', help='Specify directory of outbox')
    parser_a.add_argument('-i', '--import_var', action='store_true', help='import vcf and annotation(raw_variants.vcf)')
    parser_a.add_argument('-c', '--cross', action='store_true', help='cross vcf with annotation after import')
    parser_a.add_argument('-k', '--add_knowledge', action='store_true', help='add knownledge DB annotation')
    parser_a.add_argument('-pi', '--pass_filter_intronic', action='store_true', help="pass 'intronic' filter for annotation")
    parser_a.add_argument('-u', '--update', action='store_true', help='update import data')
    parser_a.set_defaults(func=handle_autobox)

    parser_b = subparsers.add_parser('local', help='from local')
    parser_b.add_argument('project', type=str, help='Specify Project prefix')
    parser_b.add_argument('run_bn', type=int, help='Specify RUN batch No.')
    parser_b.add_argument('pipeline', choices=['Miseq', 'cedar'], help='Specify pipeline')
    parser_b.add_argument('dir_data', help='Specify directory of data')
    parser_b.add_argument('-i', '--import_var', action='store_true', help='import vcf and annotation(raw_variants.vcf)')
    parser_b.add_argument('-u', '--update', action='store_true', help='update import data')
    parser_b.set_defaults(func=handle_local)

    args = parser.parse_args()
    if not (args.import_var or args.cross):
        parser.error('No action requested, add --import_var or --cross')

    # handle table belonging
    if args.project == '56gene':
        table_vcf = '56gene_vcf'
        table_anno = '56gene_anno'
    elif args.project in ['42geneLung', '42gene']:
        table_vcf = '42gene_vcf'
        table_anno = '42gene_anno'
    elif args.project == 'BRCA':
        table_vcf = 'BRCA_vcf'
        table_anno = 'BRCA_anno'
    elif args.project == 'ZS-BRCA':
        table_vcf = 'ZS_BRCA_vcf'
        table_anno = 'ZS_BRCA_anno'
    else:
        raise Exception('Unknown Project: %s' % args.project)

    m_con = MysqlConnector(mysql_config, 'TopgenNGS')
    args.func()
    m_con.done()
