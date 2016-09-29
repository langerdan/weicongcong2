#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : cross_SNP
# AUTHOR  : codeunsolved@gmail.com
# CREATED : September 20 2016
# VERSION : v0.0.1a

import os
import re
import sys
import xlwt
from BASE import parse_vcf
from sqlConnector import MysqlConnector
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
	for each_data in data:
		if m_con.query("SELECT id FROM 56gene_VCF "
					   "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos=%s",
					   each_data[:5]).rowcount == 1:
			#print "=>record existed!\n=>update %s" % each_data[5:]
			m_con.query("UPDATE 56gene_VCF "
						"SET RS_id=%s, Ref=%s, Alt=%s, Qual=%s, Filter=%s, Info=%s, Format=%s, "
						"Format_val=%s, AC=%s, AF=%s, AN=%s, DB=%s, DP=%s, FS=%s, MLEAC=%s, MLEAF=%s, MQ=%s, MQ0=%s, "
						"QD=%s, SOR=%s, BaseQRankSum=%s, MQRankSum=%s, ReadPosRankSum=%s, GT=%s, AD=%s, GQ=%s, PL=%s "
						"WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos=%s",
						(each_data[5:] + each_data[:5]))
			m_con.cnx.commit()
		else:
			#print "=>insert %s" % each_data
			m_con.insert(insert_g, each_data)


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
	for each_data in data:
		if m_con.query("SELECT id FROM 56gene_anno "
					   "WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos_s=%s",
					   each_data[:5]).rowcount == 1:
			#print "=>record existed!\n=>update %s" % each_data[5:]
			m_con.query("UPDATE 56gene_anno "
						"SET Pos_e=%s, Ref=%s, Alt=%s, "
			            "Func_refGene=%s, Gene_refGene=%s, ExonicFunc_refGene=%s, AAChange_refGene=%s, "
			            "phastConsElements46way=%s, genomicSuperDups=%s, esp6500si_all=%s, 1000g2014sep_all=%s, "
			            "snp138=%s, ljb26_all=%s, cg69=%s, cosmic70=%s, clinvar_20140929=%s, Otherinfo1=%s, "
			            "Otherinfo2=%s, Otherinfo3=%s "
						"WHERE Pipeline=%s AND SAP_id=%s AND RUN_bn=%s AND Chr=%s AND Pos_s=%s",
						(each_data[:5] + each_data[5:]))
			m_con.cnx.commit()
		else:
			#print "=>insert %s" % each_data
			m_con.insert(insert_g, each_data)


def query_vcf(term):
	query_g = ("SELECT Chr, Pos, RS_id, Ref, Alt, Qual, Filter, Info, Format, Format_val FROM 56gene_VCF "
	           "WHERE Pipeline=%s AND SAP_id=%s AND Chr=%s AND Pos=%s AND Ref=%s AND Alt=%s")
	return m_con.query(query_g, term)


def query_anno(term):
	query_g = ("SELECT * FROM 56gene_anno "
	           "WHERE Pipeline=%s AND SAP_id=%s AND Chr=%s AND Pos_s=%s AND Pos_e=%s AND Ref=%s AND Alt=%s")
	return m_con.query(query_g, term)


def output_cross(cross_snp_d, cross_anvc_d):
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

	path_cross_anvc = os.path.join(dir_sap, "%s_SNP.xls" % sap_id)

	workbook = xlwt.Workbook(style_compression=2)
	sheet1 = workbook.add_sheet(u'SNP', cell_overwrite_ok=True)
	sheet2 = workbook.add_sheet(sap_id, cell_overwrite_ok=True)

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

	for line_i, line in enumerate(onco_snp):
		for snp_i, snp in enumerate(line):
			sheet1.write(line_i + 1, snp_i, snp)
		for cross_snp_i, cross_snp in enumerate(cross_snp_d[line_i]):
			sheet1.write(line_i + 1, cross_snp_i + 7, cross_snp)

	for vcf_i, vcf in enumerate(vcf_col[3:13]):
		sheet2.write(0, vcf_i, vcf_col[3 + vcf_i], set_style(220, True, 'light_orange'))
	for anno_i, anno in enumerate(anno_col[3:]):
		sheet2.write(0, anno_i + 10, anno_col[3 + anno_i], set_style(220, True, 'light_green'))
		
	for line_i, line in enumerate(cross_anvc_d):
		for cross_anvc_i, cross_anvc in enumerate(line):
			sheet2.write(line_i + 1, cross_anvc_i, cross_anvc)
	workbook.save(path_cross_anvc)

if __name__ == '__main__':
	vcf_data = []
	anno_data = []
	m_con = MysqlConnector(mysql_config, 'TopgenNGS')
	for each_run in os.listdir(dir_outbox):
		if re.match(dir_prefix, each_run):
			print "<%s>" % each_run
			dir_run = os.path.join(dir_outbox, each_run)
			for each_sap in os.listdir(dir_run):
				dir_sap = os.path.join(dir_run, each_sap)
				if os.path.isdir(dir_sap):
					print "-{%s}" % each_sap
					sap_id = re.match('(.+?)[._]', each_sap).group(1)
					cross_anvc_data = []
					output_trigger = 0 if re.search('import', options) else 3
					for each_file in os.listdir(dir_sap):
						pipeline = re.search('%s(_.+_)$' % str(run_bn + offset), each_run).group(1)
						if re.search('import', options) and re.search('raw_variants\.vcf$', each_file):
							vcf_body = parse_vcf(os.path.join(dir_sap, each_file))
							for vcf_line in vcf_body:
								vcf_data.append([pipeline, sap_id, run_bn] + vcf_line + parse_info(vcf_line[-3]) + \
									  parse_format(vcf_line[-2], vcf_line[-1]))
							print "import vcf...",
							import_vcf(vcf_data)
							output_trigger |= 1
							print "OK!"

						if re.search('hg19_multianno\.txt$', each_file):
							anno_body = parse_anno(os.path.join(dir_sap, each_file))
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
										print "=cross=[%s][%s] miss match" % (each_run, sap_id)
										print "=%s" % anno_line
										cross_anvc_data.append(['', '', '', '', '', '', '', '', '', ''] + anno_line)
									else:
										cross_anvc_data.append(list(cursor.fetchone()) + anno_line)
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

								cursor_a = query_anno([pipeline, sap_id] + each_snp[:5])
								if cursor_a.rowcount != 1:
									print "\t=SNP-ANN= miss match - %s" % each_snp[:5]
									cross_snp_data[-1] += ["", "", "", "", ""]
								else:
									row_a = cursor_a.fetchone()
									cross_snp_data[-1] += list(row_a[9:13]) + [row_a[-3]]

								cursor_v = query_vcf([pipeline, sap_id] + each_snp[:2] + each_snp[3:5])
								if cursor_v.rowcount != 1:
									print "\t=SNP-VCF= miss match - %s" % each_snp[:5]
									cross_snp_data[-1] += ["", ""]
								else:
									row_v = cursor_v.fetchone()
									cross_snp_data[-1] += [row_v[-1], row_v[-2]]
							print "output cross SNP xls...",
							output_cross(cross_snp_data, cross_anvc_data)
							print "OK!"
	m_con.done()
