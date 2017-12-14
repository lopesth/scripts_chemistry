#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Python 2.7

Created on 09:27 BRST 01 May 2017

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Calculo de BLA

"""
import numpy, os, math

def find_a_position(file_name, string):
	positions =[]
	file = open(file_name, "r")
	for num, line in enumerate(file, 1):
		if string in line:
			positions.append(num)
	return positions

def take_the_CP_data(file_name, cp_list, descriptor):
	temp_final = []
	for cp in cp_list:
		temp = []
		file = open(file_name, "r")
		lookup1 = "================   CP    " + str(cp)
		lookup2 = "================   CP    " + str(cp+1)
		position_start = find_a_position(file_name, lookup1)[-1]
		position_end = find_a_position(file_name, lookup2)[-1]
		pos = len(descriptor.split())
		for num, line in enumerate(file, 1):
			if num in range(position_start, position_end, 1):
				if descriptor in line:
					temp = (float(line.split()[pos]))

		temp_final.append(temp)
	return temp_final

# lista com as moléculas_base e seus números de átomos, ligações simples e ligações duplas
molecules_completed_list = {"case1_5C": [[21, 25],[24, 26]], "case2_5C": [[22, 25],[23, 27]], "case3_5C": [[21, 25],[24, 26]], "case1_9C": [[ 30, 33, 37, 42],[ 31, 36, 40, 43]], "case2_9C": [[ 30, 33, 37, 41],[ 31, 35, 39, 43]], "case3_9C": [[ 30, 33, 37, 42],[ 31, 36, 40, 43]]}
molecules = ["5C", "9C"]
cases = ["case1", "case2", "case3"]
list_of_descriptors = ["Density of all electrons", "Laplacian of electron density", "Electron localization function (ELF)", "Ellipticity of electron density"]

home = os.popen('pwd').read().split()[0]

for case in cases:

	for molecule in molecules:
		fields = []
		if molecule == "5C":
			field_temp = numpy.arange(0,146,9.12)
		if molecule == "9C":
			field_temp = numpy.arange(0,88,5.48)
		for field_elem in range(0, len(field_temp)):
			fields.append(str(round(field_temp[field_elem], 0)).split('.')[0])
		for descriptor in list_of_descriptors:
			descriptor_name = "".join(("".join("".join(descriptor.split("(")).split(")"))).split())
			file_target = open(home+"/"+case+"/"+"qtaim_"+case+"_" + molecule + "_" + descriptor_name +".txt", "w")
			for field in fields:
				if case == "case1":
					name_file = home+"/"+case+"/"+molecule+"/Form_Checkpoint/"+"pre_opt_"+case+"_" + molecule + "_" + field + "_CPprop.txt"
				else:
					name_file = home+"/"+case+"/"+molecule+"/Form_Checkpoint/"+"boa_"+case+"_" + molecule + "_" + field + "_CPprop.txt"
				mean_by_bond = []
				for cp_list in molecules_completed_list[case+"_"+molecule]:
					cp_data = take_the_CP_data(name_file, cp_list, descriptor)
					mean_temp = 0
					for a in range(0, len(cp_data), 1):
						mean_temp = mean_temp + cp_data[a]
					mean_by_bond.append(mean_temp / len(cp_data))
				mean = (mean_by_bond[0] - mean_by_bond[1])/2

				file_target.write("%-7s %.7f\n" %(field, mean))
			file_target.close()











