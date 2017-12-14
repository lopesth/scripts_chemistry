#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Python 2.7

Created on Mar 21 21:29 BRST 2017

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Optimization of the streptocianine

"""

import numpy

molecules = ["13C"]

for molecule in molecules:
	fields = []
	if molecule == "5C":
		field_temp = numpy.arange(0,146,9.12)
	if molecule == "9C":
		field_temp = numpy.arange(0,88,5.48)
	if molecule == "13C":
		field_temp = numpy.arange(0,91,3)
	for field_elem in range(0, len(field_temp)):
		fields.append(str(round(field_temp[field_elem], 0)).split('.')[0])
	for field in fields:
		name_file = "pre_opt_case1_" + molecule + "_" + field
		file_com = open(name_file + '.com', 'w')
		file_com.write('%schk=%s.chk \n%snprocshared=2 \n%smem=2000mb \n' %("%", name_file,"%", "%") )
		file_com.write('#p opt=(CalcFC, gdiis,z-matrix) nosymm field=X+%s output=wfn b3lyp/3-21G\n\nOptimization of the streptocianine_%s molecule in field %s in the X direction\n\n1 1\n' %(field, molecule, field))
		with open(molecule+'.geom') as geom_file:
			for line in geom_file:
				file_com.write(line)
			geom_file.close()
		file_com.write('\n\n%s.wfn\n\n\n' %(name_file))
		file_com.close()
