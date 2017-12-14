#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Python 2.7

Created on Sat, 19 Aug  15:56h BRST 2017

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Script para verificar se o Dice termalizou um arquivo
"""

def line_range(input_file, str_begin, str_end):
	temp_begin = []
	temp_end = []
	with open(input_file) as myFile:
		for num, line in enumerate(myFile, 1):
			if str_begin in line:
				temp_begin.append(num)
			if str_end in line:
				temp_end.append(num)
	return (temp_begin[-1], temp_end[-1])

def take_a_lines_in_series(input_file, range_to_take):
	lines_of_interest = []
	with open(input_file) as myFile:
		for num, line in enumerate(myFile, 1):
			if num <= int(range_to_take[0])+1:
				pass
			elif num >= int(range_to_take[1]):
				pass
			else:
				lines_of_interest.append(line.split())
	return lines_of_interest

def take_a_order_element_in_list_of_list(prime_list, order_element):
	elements_of_interest = []
	for sec_list in prime_list:
		elements_of_interest.append(sec_list[order_element])
	return elements_of_interest

def verify_termalization(file_to_check):
	last_energy = take_a_order_element_in_list_of_list(take_a_lines_in_series(file_to_check, line_range(file_to_check, "Start cooling process", "End   cooling process")), 2)[-1]
	if float(last_energy) > 0:
		return [False, last_energy]
	else:
		return [True, last_energy]

if __name__ == "__main__":
	import os
	contador = 0
	for group_molecule in ["1", "2", "3"]:
		for molecule_sub in ["A", "B", "C"]:
			for isomer in ["E", "Z"]:
				for solvent in ["DMSO", "EtOH", "MeCl3", "MeOH", "PropO", "THF"]:
					molecule = group_molecule + molecule_sub + isomer + solvent
					dir_home = os.popen("pwd").read().split()[0]
					anchor = verify_termalization(dir_home + "/"+ group_molecule + molecule_sub + isomer +"/"+ solvent +"/"+molecule+".ter.out")
					if anchor[0] == False:
						print ("O arquivo %s não termalizou, energia ficou em %s" %(molecule, anchor[1]))
						contador = contador + 1
					else:
						pass
	print ("No total %d moleculas não termalizaram." %contador)
	
					