#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Python 2.7

Created on 09:27 BRST 01 May 2017

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Calculo de BLA

"""
import numpy, os, math

def take_bond_order(basis, file_name):
	list_of_bo = []
	rouded_basis = basis
	counter = 0
	while ((rouded_basis + counter) % 5) != 0:
		counter = counter + 1
	rouded_basis = rouded_basis + counter
	for turn in range (0, basis, 1):
		file = open(file_name, "r")
		temp_list = []
		positions = range(4+turn, (rouded_basis/5)*(basis+1)+3 ,basis + 1)
		for num, line in enumerate(file, 1):
			if num in positions:
				temp = line.split()
				for x in range(1, len(temp), 1):
					try:
						temp_list.append(temp[x])
					except Exception as e:
						pass
		list_of_bo.append(temp_list)
		file.close()
	return list_of_bo

def filter_BO_interest(list_bo, bonds):
	bond_orders = []
	for bonds in bonds:
		atom1 = int(bonds.split("-")[0])
		atom2 = int(bonds.split("-")[1])
		bond_orders.append((list_bo[atom1-1])[atom2-1])
	return bond_orders

def media_of_bond_goups(list_bo):
	number_of_bonds = len(list_bo)
	bond = 0
	for turn in range(0, number_of_bonds, 1):
		bond = bond + float(list_bo[turn])
	mean = bond / number_of_bonds
	return mean


# lista com as moléculas_base e seus números de átomos, ligações simples e ligações duplas
molecules = {
"5C": [[16],["1-3", "5-7"],["3-5", "9-7"]],
"9C": [[24],["15-12", "1-3", "5-7", "9-11"],["12-1", "3-5", "7-9", "11-13"]]
}

cases = ["case2", "case1", "case3"]
home = os.popen('pwd').read().split()[0]
types = ["mulliken", "mayer", "wiberg"]

for case in cases:
	for type in types:
		for molecule in molecules.keys():
			bo_file = open(home+"/"+case+"/"+case+"_" + molecule + "_" + type+"_bo_all.txt", "w")
			atons_number = ((molecules[molecule])[0])[0]
			fields = []
			if molecule == "5C":
				field_temp = numpy.arange(0,146,9.12)
			if molecule == "9C":
				field_temp = numpy.arange(0,88,5.48)
			if molecule == "13C":
				field_temp = numpy.arange(0,91,3)
			for field_elem in range(0, len(field_temp)):
				fields.append(str(round(field_temp[field_elem], 0)).split('.')[0])
			file_target = open(home+"/"+case+"/"+"boa_"+case+"_" + molecule + "_" + type+".txt", "w")
			for field in fields:
				name_file = home+"/"+case+"/"+molecule+"/BO_files/"+"boa_"+case+"_" + molecule + "_" + field + "_bndmat_"+type+".txt"
				bond_orders = take_bond_order(atons_number, name_file)
				singles = filter_BO_interest(bond_orders, (molecules[molecule])[1])
				doubles = filter_BO_interest(bond_orders, (molecules[molecule])[2])
				boa_alternation = media_of_bond_goups(singles) - media_of_bond_goups(doubles)
				if case == "case2":
					factor = -1
				else:
					factor = 1
				file_target.write("%-7s %.5f\n" %(field, factor*boa_alternation))
				bo_file.write("Field %s:\n\n" %field)	
				for i in range(0, len(singles)):
					bo_file.write("%-10s %10s\n" %("Simples" + str(i +1), singles[i]))
					bo_file.write("%-10s %10s\n" %("Dupla" + str(i +1), doubles[i]))
				bo_file.write("_______________________\n")
				bo_file.write("\n\n")
			file_target.close()
			bo_file.close()
			