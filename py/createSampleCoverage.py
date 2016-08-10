#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM  : createSampleCoverageData_v0.01a
# PURPOSE  :
# AUTHOR   : codeunsolved@gmail.com
# CREATED  : August 10 2016

import os
import re
import json
from BASE import read_bed
from BASE import clean_output

# CONFIG AREA #
path_bed = r'/Users/codeunsolved/Downloads/NGS-data/bed/onco-1606-probes-depth.bed'
dir_depth_data = r'/Users/codeunsolved/Downloads/NGS-data/onco'
dir_output = r'/Users/codeunsolved/NGS/Topgen-Dashboard/data/onco'


