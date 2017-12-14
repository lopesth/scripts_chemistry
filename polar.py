#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Python 2.7

Created on 12:43 BRST 01 May 2017

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Title

"""
import os, numpy, math

def number_of_a_lookup(file_name, lookup):
	positions = []
	file = open(file_name, "r")
	for num, line in enumerate(file, 1):
		if lookup in line:
			positions.append(int(num))
	file.close()
	return positions

def NLO(file_name, start_number, end_number):
	file_temp = [] 
	interval = range(start_number,end_number, 1)
	file = open(file_name, "r")
	for num, line in enumerate(file, 1):
		if num in interval:
			file_temp.append(line)
	file.close()
	for element in range(0, len(file_temp), 1):
		if " Dipole polarizability, Alpha (input orientation)." in file_temp[element]:
			alpha_number = element
		if " First dipole hyperpolarizability, Beta (input orientation)." in file_temp[element]:
			beta_number = element
		if " Second dipole hyperpolarizability, Gamma (input orientation)." in file_temp[element]:
			gama_number = element
	dipole_temp = (file_temp[4]).split()[2]
	dipole = dipole_temp.split('D')[0]+"E"+dipole_temp.split('D')[1]
	alpha_temp = (file_temp[alpha_number+6]).split()[2]
	alpha = alpha_temp.split('D')[0]+"E"+alpha_temp.split('D')[1]
	beta_temp = (file_temp[beta_number+12]).split()[2]
	beta = beta_temp.split('D')[0]+"E"+beta_temp.split('D')[1]
	gama_temp = (file_temp[gama_number+8]).split()[2]
	gama = gama_temp.split('D')[0]+"E"+gama_temp.split('D')[1]
	return float(dipole), float(alpha), float(beta), float(gama)


molecules = ["13C"]
cases = ["case1", "case2", "case3"]
home = os.popen('pwd').read().split()[0]

for case in cases:
	for molecule in molecules:
		file_target = open(case+"/"+case+"_"+molecule+"_polar.txt", "w")
		file_target.write("%20s %20s %5s %20s %5s %20s %5s %20s\n" %("Molecule", "Dipole Momente (D)", "", "Alpha (10**-24 esu)", "", "Beta (10**-30 esu)", "", "Gama (10**-36 esu)"))
		fields = []
		dipole_list = []
		alpha_list = []
		beta_list = []
		gama_list = []
		if molecule == "5C":
			field_temp = numpy.arange(0,146,9.12)
		if molecule == "9C":
			field_temp = numpy.arange(0,88,5.48)
		if molecule == "13C":
			field_temp = numpy.arange(0,91,3)
		for field_elem in range(0, len(field_temp)):
			fields.append(str(round(field_temp[field_elem], 0)).split('.')[0])
		for field in fields:
			name_file = home+"/"+case+"/"+molecule+"/Output/"+"polar_"+case+"_" + molecule + "_" + field+ ".log"

			start_number = number_of_a_lookup(name_file, " Electric dipole moment (input orientation):")[0]
			end_number = number_of_a_lookup(name_file, " Dipole orientation:")[0] - 3
			nlo_temp = NLO(name_file, start_number, end_number)
			file_target.write("%20s %20.5f %5s %20.5f %5s %20.5f %5s %20.5f\n" %((name_file.split("/")[-1]).split(".")[0], nlo_temp[0], "", nlo_temp[1], "", nlo_temp[2], "", nlo_temp[3]))

		file_target.close()















