#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Python 2.7

Created on Sat, 19 Aug  15:56h BRST 2017

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Script para criar o inputs da CEPS B80
"""

import os, numpy

def make_geom_list(file, list_to_lock):
	lista_temp_mae = []
	with open(file) as myFile:
		for num, line in enumerate(myFile, 1):
			if len(line) > 2:
				list_temp = []
				if len(line.split()) > 4:
					text = 'Arquivo de geometria ('+file+') com defeito'
					raise Exception(text)
				list_temp.append(line.split()[0])
				if num in list_to_lock:
					list_temp.append("-1")
				else:
					list_temp.append("0")
				list_temp.append(float(line.split()[1]))
				list_temp.append(float(line.split()[2]))
				list_temp.append(float(line.split()[3]))
				lista_temp_mae.append(list_temp)
	return lista_temp_mae

if __name__ == "__main__":

	base_list = {"B80_h": [71], "B80_p": [81]}
	gas_list = {"NH3":[1], "SH2":[2], "CO2":[1], "SO2":[3], "H2":[2], "HF":[2]}
	master_dir = os.popen("pwd", "r").read().split()[0]
	range_mol = numpy.arange(5.8, 12.1, 0.2)
	porcentagem = "%"
	level_of_theory = "b3lyp"
	comentario = "Cálculo de otimizacao da CEP do"
	multiplicidade = "0 1"
	complemento = "relax_w_freeze_atoms"
	resp_base_mista = "yes"

	if resp_base_mista == "yes":
		elements_solute = {"B" : "B"}
		elements_gas = {}
		for gas in gas_list.keys():
			element_gas = []
			y = list(gas)
			for y_element in y:
				try:
					yy = int(y_element)
				except:
					element_gas.append(y_element)
			elements_gas.update({gas : element_gas})
		basis_to_use = { "6-31G(d,p)" : elements_gas, "LANL2DZ" : elements_solute}
	
	for base in base_list.keys():
		lista_geom_b80 = make_geom_list(master_dir + "/geom/"+base+".geom", base_list[base])
	
		for gas in gas_list.keys():
			lista_geom_gas = make_geom_list(master_dir + "/geom/"+gas+".geom", gas_list[gas])
			for inc in range_mol:
				nome_input = "opt_" + base + "_" + gas + "_R" + str(inc) + "_" + complemento
				file_to_write = open(master_dir + "/" + gas + "/" + nome_input+".com", "w")
				file_to_write.write("%schk=%s.chk\n%snprocshared=4\n%smem=2000mb\n" %(porcentagem, nome_input, porcentagem, porcentagem))
				if resp_base_mista == "yes":
					file_to_write.write("#p opt nosymm %s/genecp\n\n%s %s_%s_%s\n\n%s\n" %(level_of_theory, comentario, base, gas, inc, multiplicidade))
				else:
					file_to_write.write("#p opt nosymm %s\n\n%s %s_%s_%s\n\n%s\n" %(level_of_theory, comentario, base, gas, inc, multiplicidade))
				for linha_geom in lista_geom_b80:
					file_to_write.write( "%-15s %2s %12.6f %12.6f %12.6f\n" %(linha_geom[0], linha_geom[1], linha_geom[2], linha_geom[3], linha_geom[4]))
				for linha_geom in lista_geom_gas:
					file_to_write.write( "%-15s %2s %12.6f %12.6f %12.6f\n" %(linha_geom[0], linha_geom[1], linha_geom[2], linha_geom[3], linha_geom[4]+inc))
				file_to_write.write("\n")
				if resp_base_mista == "yes":
					for x in range (0, len(basis_to_use), 1):
						try:
							anchor = " ".join((basis_to_use.values()[x])[elements_solute.keys()[0]])
						except:
							anchor = " ".join((basis_to_use.values()[x])[gas])
						file_to_write.write("%s 0\n" %(anchor))
						file_to_write.write("%s\n" %basis_to_use.keys()[x])
						file_to_write.write("%s\n" %("****"))
						if x == 1:
							file_to_write.write("\n%s 0\n" %(anchor))
							file_to_write.write("%s\n" %basis_to_use.keys()[x])
				file_to_write.write("\n\n")

						


