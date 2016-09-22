import os
import re

dir_data = r'/Users/codeunsolved/Downloads/NGS-Data'
project = "BRCA"

already_had = {
	"BRCA": ['BRCA160107', 'BRCA160313', 'BRCA160320', 'BRCA160406', 'BRCA160408', 'BRCA160427', 'BRCA160517',
			 'BRCA160601', 'BRCA160708', 'BRCA160724', 'BRCA160724-2', 'BRCA160727',
			 'BRCA160811', 'BRCA160819', 'BRCA160824', 'BRCA160830'],
	"onco": []
}

proj_table = {}
for each_dir in os.listdir(dir_data):
	dir_run = os.path.join(dir_data, each_dir)
	if re.match('%s' % project, each_dir) and os.path.isdir(dir_run) and each_dir not in already_had["BRCA"]:
		print "=>%s" % dir_run
		run_bn = re.match('%s(.+)' % project, each_dir).group(1)
		proj_table[run_bn] = []
		for each_file in os.listdir(dir_run):
			if re.search('\.bam$', each_file):
				basename = re.match('(.+)\.bam', each_file).group(1)
				if re.search('_S\d+', basename):
					basename = re.match('(.+)_S\d+', each_file).group(1)
				proj_table[run_bn].append(basename)
		print proj_table[run_bn]

with open('/Users/codeunsolved/Downloads/NGS-Data/DB/%s_lab-2.csv' % project, 'wb') as w_obj:
	proj_table_sorted = sorted(proj_table.iteritems(), key=lambda d: d[0])
	for key, value in proj_table_sorted:
		for sample_id in value:
			w_obj.write(',%s,unknown,,,,,,,,,,,,,,,,,,,,,%s,,,,,,INIT\n' % (sample_id, key))
