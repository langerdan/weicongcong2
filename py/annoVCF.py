#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : annoVCF
# AUTHOR  : codeunsolved@gmail.com
# CREATED : September 18 2016
# UPDATE  : v0.0.1a

import os
import re
import json
import time
from BASE import clean_output
from BASE import parse_vcf
from sqlConnector import MysqlConnector
from config import mysql_config

dir_vcf = r'/Users/codeunsolved/Downloads/NGS-Data/Report-fusion_gene/=TEMP=/BRCA160320/normVCF'
dir_output = r'/Users/codeunsolved/NGS/Topgen-Dashboard/data/BRCA160320'
vcf_suffix = 'step2\.vcf'


def query_clinvar(data):
	query_g = ("SELECT Chr, Pos_S, Pos_E, Ref, Alt, CLINSIG FROM hg19_clinvar_20160302_origin "
			   "WHERE Chr=%s AND Pos_S=%s AND Ref=%s AND Alt=%s")
	return m_con.query(query_g, data)


def output_anno(data, filename):
	with open(os.path.join(dir_output_vcf, '%s.anno' % filename), 'wb') as w_obj:
		w_obj.write(json.dumps(data))


def input_mysql(data):
	insert_g = ("INSERT INTO ANNO "
				"(Project, SAP_id, RUN_bn, Path) "
				"VALUES (%s, %s, %s, %s)")
	for each_data in data:
		if m_con.query("SELECT id FROM ANNO "
					   "WHERE Project=%s AND SAP_id=%s AND RUN_bn=%s",
					   each_data[:3]).rowcount == 1:
			print "=>record existed!\n=>update %s" % each_data[3]
			m_con.query("UPDATE ANNO "
						"SET Path=%s "
						"WHERE Project=%s AND SAP_id=%s AND RUN_bn=%s",
						(each_data[3], each_data[0], each_data[1], each_data[2]))
			m_con.cnx.commit()
		else:
			print "=>insert %s" % each_data
			m_con.insert(insert_g, each_data)


clean_output(dir_output, "annotation")
dir_output_vcf = os.path.join(dir_output, "annotation")
time_start = time.time()

m_con = MysqlConnector(mysql_config, 'TopgenNGS')
vcf_files = os.listdir(dir_vcf)
mysql_data = []
data_basename = os.path.basename(os.path.dirname(dir_vcf))
if re.search('BRCA', data_basename):
	project = 'BRCA'
elif re.search('onco', data_basename):
	project = '56gene'
else:
	project = 'unknown'
run_bn = data_basename
if re.match('BRCA|onco', run_bn):
	run_bn = re.match('(?:BRCA|onco)(.+)', run_bn).group(1)

i = 0
for vcf_file in vcf_files:
	if re.search('^[\dWD].+%s$' % vcf_suffix, vcf_file):
		sap_id = re.match('(.+)%s$' % vcf_suffix, vcf_file).group(1)
		if re.search('_S\d+', sap_id):
			sap_id = re.match('(.+)_S', sap_id).group(1)
		table_head = ["Chr", "Start", "End", "Ref", "Alt", "Clinvar"]
		output = [table_head]
		i += 1
		print "=>%s" % vcf_file
		path_vcf = os.path.join(dir_vcf, vcf_file)
		vcf = parse_vcf(path_vcf)
		for variant in vcf:
			variant_anno = []
			print "\t%s-%s-%s-%s" % (variant[0], variant[1], variant[3], variant[4])
			variant_anno = [variant[0], variant[1], variant[1], variant[3], variant[4]]

			# annotate clinvar
			cursor = query_clinvar((variant[0], variant[1], variant[3], variant[4]))
			if cursor.rowcount:
				row = cursor.fetchone()
				print "\t\t{Clinvar}%s" % [str(x) for x in row]
				variant_anno.append(list(row)[-1])
				if cursor.rowcount > 1:
					print "\t\t{Clinvar} [WARNING] multiple matches!"
			else:
				variant_anno.append("")
			output.append(variant_anno)
		output_anno(output, sap_id)
		mysql_data.append([project, sap_id, run_bn, "data/%s/annotation/%s.anno" % (data_basename, sap_id)])


print "insert data..."
input_mysql(mysql_data)
print "OK!"
m_con.done()
print "====== Done ======\nTotal VCF: %d\t Time: %ss" % (i, time.time() - time_start)
