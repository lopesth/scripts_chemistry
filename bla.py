#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Python 2.7

Created on 09:27 BRST 01 May 2017

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Calculo de BLA

"""
import numpy, os, math

def interval_number_of_a_lookup(file_name, lookup1, lookup2):
	file = open(file_name, "r")
	for num, line in enumerate(file, 1):
		if lookup1 in line:
			position_initial = int(num) + 5
		if lookup2 in line:
			position_final = int(num)
	file.close()
	interval = range(position_initial, position_final, 1)
	return interval

def take_position(file_name):
	atomic_number = []
	atom_order = []
	atom_x = []
	atom_y = []
	atom_z = []
	lookup1 = 'Input orientation:'
	lookup2 = '---------------------------------------------------------------------'
	file_number = interval_number_of_a_lookup(file_name, lookup1, lookup2)

	file = open(file_name, "rb")
	for num, line in enumerate(file, 1):
		if (num in file_number):
			list_take = line.split()
			atom_order.append(int(list_take[0]))
			atomic_number.append(int(list_take[2]))
			atom_x.append(float(list_take[3]))
			atom_y.append(float(list_take[4]))
			atom_z.append(float(list_take[5]))
	file.close()

	return atom_order, atomic_number, atom_x, atom_y, atom_z

def distance_between_2_points (x1, x2, y1, y2, z1, z2):
	distance = math.sqrt( math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2) + math.pow((z2 - z1), 2) )
	return distance

def bond_distance(bond_list):
	Bonds_length = {}
	for bond in bond_list:
		atom1 = int(bond.split("-")[0])-1
		atom2 = int(bond.split("-")[1])-1
		distance = distance_between_2_points((atom_coord[2])[atom1], (atom_coord[2])[atom2], (atom_coord[3])[atom1], (atom_coord[3])[atom2], (atom_coord[4])[atom1], (atom_coord[4])[atom2])
		Bonds_length.update({bond : distance})
	return Bonds_length

def BLA_calc(single_bonds, double_bonds):
	value_single = 0
	value_double = 0
	for number in range(0,len(single_bonds), 1):
		value_single = value_single + single_bonds.values()[number]
	for number in range(0,len(double_bonds), 1):
		value_double = value_double + double_bonds.values()[number]
	bla_result = (value_single / len(single_bonds)) - (value_double / len(double_bonds))
	return bla_result


molecules = ["9C", "5C"]
cases = ["case2", "case3"]
home = os.popen('pwd').read().split()[0]

for case in cases:
	for molecule in molecules:
		file_target = open(case+"/"+case+"_"+molecule+"_bla.txt", "w")
		fields = []
		if molecule == "5C":
			field_temp = numpy.arange(0,146,9.12)
			BLA_double_index = ["3-5", "7-9"]
			BLA_single_index = ["1-3", "5-7"]
		if molecule == "9C":
			field_temp = numpy.arange(0,88,5.48)
			BLA_double_index = ["12-1", "3-5", "7-9", "11-13"]
			BLA_single_index = ["15-12", "1-3", "5-7", "9-11"]
		if molecule == "13C":
			field_temp = numpy.arange(0,91,3)
			BLA_double_index = ["20-15", "12-1", "3-5", "7-9", "11-13", "19-23"] 
			BLA_single_index = ["24-20", "15-12", "1-3", "5-7", "9-11", "13-19"]
		for field_elem in range(0, len(field_temp)):
			fields.append(str(round(field_temp[field_elem], 0)).split('.')[0])
		for field in fields:
			name_file = "boa_"+case+"_" + molecule + "_" + field
			atom_coord = take_position(home+"/"+case+"/"+molecule+"/Output/"+name_file + ".log")
			
			BLA_single_length = bond_distance(BLA_double_index)
			BLA_double_length = bond_distance(BLA_single_index)
	
			bla = BLA_calc(BLA_single_length, BLA_double_length)
			if case == "case2":
				factor = -1
			else:
				factor = 1
			
			file_target.write("%-25s %.5f\n" %(name_file, factor*bla))
		file_target.close()











