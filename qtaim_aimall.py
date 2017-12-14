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

def take_the_CP_data(file_name, cp_raw, descriptor):
	cp = cp_raw.split(" - ");
	temp_final = []
	temp = []
	file = open(file_name, "r")
	lookup1 = "Type = (3,-1) BCP "+cp[0]+" "+cp[1]
	lookup2 = "Type = (3,-1) BCP "+cp[1]+" "+cp[0]
	positions = find_a_position(file_name, lookup1)
	if len(positions) < 1:
		positions = find_a_position(file_name, lookup2)
	position_start = positions[0] -1
	position_end = positions[0] + 33
	for num, line in enumerate(file, 1):
		if num in range(position_start, position_end, 1):
			if descriptor in line:
				temp = float((line.split('\n')[0]).split(descriptor)[-1])
	return temp

# lista com as moléculas_base e seus números de átomos, ligações simples e ligações duplas

molecules = ["9C", "5C"]
cases = ["case1", "case2", "case3"]
list_of_descriptors = [" Bond Ellipticity =", "DelSqRho =", "   Rho ="]

home = os.popen('pwd').read().split()[0]

for case in cases:

	for molecule in molecules:
		be_file = open(home+"/"+case+"/"+"qtaim_"+case+"_" + molecule + "_" + "be_all.txt", "w")
		fields = []
		if molecule == "5C":
			molecules_completed_list = {"singles": ["C7 - C5", "C3 - C1"], "doubles": ["C9 - C7", "C5 - C3"]}
			field_temp = numpy.arange(0,146,9.12)
		if molecule == "9C":
			molecules_completed_list = {"singles": ["C12 - C15", "C3 - C1", "C7 - C5", "C11 - C9"], "doubles": ["C1 - C12", "C5 - C3", "C9 - C7", "C13 - C11"]}
			field_temp = numpy.arange(0,88,5.48)
		if molecule == "13C":
			molecules_completed_list = {"singles": ["C20 - C24", "C12 - C15", "C3 - C1", "C7 - C5", "C11 - C9", "C19 - C13"], "doubles": ["C15 - C20", "C1 - C12", "C5 - C3", "C9 - C7", "C13 - C11", "C23 - C19"]}
			field_temp = numpy.arange(0,91,3)
		for field_elem in range(0, len(field_temp)):
			fields.append(str(round(field_temp[field_elem], 0)).split('.')[0])
		for descriptor in list_of_descriptors:
			descriptor_name = ("".join(("".join("".join(descriptor.split("(")).split(")"))).split())).split("=")[0]
			file_target = open(home+"/"+case+"/"+"qtaim_"+case+"_" + molecule + "_" + descriptor_name +".txt", "w")
			for field in fields:
				if case == "case2":
					name_file = home+"/"+case+"/"+molecule+"/BO_files/"+"boa_"+case+"_" + molecule + "_" + field + ".sum"
				else:
					name_file = home+"/"+case+"/"+molecule+"/BO_files/"+"boa_"+case+"_" + molecule + "_" + field + ".sum"
				mean_by_bond = []
				cp_data_singles = []
				cp_data_doubles = []
				for cp in molecules_completed_list["singles"]:
					cp_data_singles.append(take_the_CP_data(name_file, cp, descriptor))
				for cp in molecules_completed_list["doubles"]:
					cp_data_doubles.append(take_the_CP_data(name_file, cp, descriptor))
				descriptor_alternation = numpy.mean(cp_data_singles) - numpy.mean(cp_data_doubles)
				if case == "case2":
					factor = -1
				else:
					factor = 1
				file_target.write("%-7s %.7f\n" %(field, factor*descriptor_alternation))
					
				if descriptor == " Bond Ellipticity =":
					be_file.write("Field %s:\n\n" %field)	
					for i in range(0, len(cp_data_singles)):
						be_file.write("%-10s %10s\n" %("Simples" + str(i +1), cp_data_singles[i]))
						be_file.write("%-10s %10s\n" %("Dupla" + str(i +1), cp_data_doubles[i]))
					be_file.write("_______________________\n")
					be_file.write("\n\n")
					
					
			file_target.close()
