#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Python 2.7

Created on Mar 21 21:29 BRST 2017

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Optimization of the streptocianine

"""

import numpy

molecules = ["squaraine-H-NMe2","squaraine-NMe2-NMe2","squaraine-OMe-H","squaraine-OMe-NMe2","squaraine-OMe-OMe","squaraine_H-H","squaraine_OH-OH","stilbene_H-H","stilbene_O-OH","stilbene_OH-OH"]

for molecule in molecules:
	name_file = "pre_opt_" + molecule
	file_com = open(name_file + '.com', 'w')
	file_com.write('%schk=%s.chk \n%snprocshared=2 \n%smem=2000mb \n' %("%", name_file,"%", "%") )
	file_com.write('#p opt nosymm b3lyp/3-21G\n\nOptimization of the %s \n\n0 1\n' %(molecule))
	with open(molecule+'.geom') as geom_file:
		for line in geom_file:
			file_com.write(line)
		geom_file.close()
	file_com.close()
