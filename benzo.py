# -*- coding: UTF-8 -*-
"""
Python 2.7

Created on Thu Jan 19 11:30:34 BRST 2017

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Small Script to Process Benzoselenodiols Photophysics Results

"""

import os

def dipole_process(name):
	file_log = open(name+'.log','r')
	for num, line in enumerate(file_log, 1):
		if ' X=             ' in line:
			dipoles.append(line.split()[7])
	file_log.close()
	return dipoles[-1]

def orbital_process(name):
	occ_orbitals1 = []
	file_log = open(name+'.log','r')
	number_line = []
	for num, line in enumerate(file_log, 1):
		if 'Alpha  occ. eigenvalues --' in line:
			occ_orbitals.append(line.split()[4:])
			number_line.append(num + 1)
	file_log = open(name+'.log','r')
	for num, line in enumerate(file_log, 1):
		if num == number_line[-1]:
			virtual_orbitals.append(line.split()[4:7])
	file_log = open(name+'.log','r')
	for num, line in enumerate(file_log, 1):
		if 'alpha electrons' in line:
			homo_number = line.split()[0]
	occ_orbitals1.append((occ_orbitals[-2] + occ_orbitals[-1])[-3:])
	return {'HOMO-2' : float((occ_orbitals1[0])[0])*27, 'HOMO-1' : float((occ_orbitals1[0])[1])*27, 'HOMO' : float((occ_orbitals1[0])[2])*27, 'LUMO' : float((virtual_orbitals[0])[0])*27, 'LUMO+1' : float((virtual_orbitals[0])[1])*27, 'LUMO+2' : float((virtual_orbitals[0])[2])*27, 'Homo #' : homo_number}

def orbital_cont(name):
	file_log = open(name+'.log','r')
	number_line = []
	w = []
	for num, line in enumerate(file_log, 1):
		if ' Excited State   1' in line:
			oscillator_force = line.split()[8]
			wavelength = line.split()[6]
			number_line1 = (num + 1)
		if 'This state for optimization' in line:
			number_line2 = (num)
	number_line = range(number_line1, number_line2)
	file_log = open(name+'.log','r')
	for num, line in enumerate(file_log, 1):
		if num in number_line:
			line_list.append([line.split()[0], (line.split()[1].split('->'))[1], line.split()[2]])

	return (oscillator_force.split('f=')[1], wavelength, line_list)

def print_values():
	result_file.write('Momento de Dipolo:   %5s D\n\n' %(dipole_moment))
	result_file.write('Orbitais de Fronteira:	%d (HOMO) e %d (LUMO)\n\n' %(int(orbitals['Homo #']), int(orbitals['Homo #'])+1))
	result_file.write('		LUMO+2  :  %8s eV\n' %((orbitals['LUMO+2'])))
	result_file.write('		LUMO+1  :  %8s eV\n' %((orbitals['LUMO+1'])))
	result_file.write('		LUMO    :  %8s eV\n' %((orbitals['LUMO'])))
	result_file.write('		HOMO    :  %8s eV\n' %((orbitals['HOMO'])))
	result_file.write('		HOMO-1  :  %8s eV\n' %((orbitals['HOMO-1'])))
	result_file.write('		HOMO-2  :  %8s eV\n\n' %((orbitals['HOMO-2'])))
	result_file.write('Band-Gap:            %5s eV\n\n\n' %(bandgap))

def contrib_values():
	result_file.write('Primeiro Estado de Excitação (S1):\n\n')
	result_file.write('		Força de Oscilador  :  %4s \n' %(dic_exc['Oscillator Force']))
	result_file.write('		Comprimento de Onda :  %6s nm \n\n' %(dic_exc['Wavelength']))
	percent = '%'
	result_file.write('		Contribuição:\n')
	single_list_number = 1
	for single_list in y[2]:
		result_file.write('		                       %s -> %s   :   %.2f%s\n' %(dic_exc['Orbital Source %s' %(single_list_number)], dic_exc['Target Orbital %s' %(single_list_number)], dic_exc['Contribution %s' %(single_list_number)], percent))
		single_list_number=1+single_list_number
	result_file.write('\n\n')

work_dir = os.getcwd()
solvents = ['agua', 'gas']
states = ('otimizacao', 'single_point')
molecules = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
methods = ['B3LYP', 'CAM-B3LYP', 'M062X', 'PBE1PBE', 'wB97XD']

result_file = open('Results.txt', 'w')
result_file.write('')
for state_dir in states:
	if state_dir == 'otimizacao':
		result_file.write('\n')
		result_file.write('--------------------------------------------- ESTADO FUNDAMENTAL (S0) ---------------------------------------------\n\n\n')
	if state_dir == 'single_point':
		result_file.write('\n')
		result_file.write('------------------------------------------ ESTADO SINGLETO EXCITADO (S1) ------------------------------------------\n\n\n')
	for solvent in solvents:
		if solvent == 'agua' :
			result_file.write('                                         -------------- ÁGUA --------------\n\n\n')
		if solvent == 'gas' :
			result_file.write('                                         -------------- VÁCUO --------------\n\n\n')

		for molecule in molecules:
			result_file.write('------------- MOLÉCULA %s -------------\n\n' %(molecule))
			if state_dir is 'single_point':
				for method in methods:
					line_list = []
					result_file.write(' --- %s ---\n\n' %(method))
					os.chdir(work_dir+'/'+state_dir+'/'+solvent+'/'+method)
					proc_name = 'bsd_'+molecule+'_sp_'+method
					dipoles = []
					dipole_moment = dipole_process(proc_name)
					occ_orbitals = []
					virtual_orbitals = []
					orbitals = orbital_process(proc_name)
					bandgap = orbitals['LUMO'] - orbitals['HOMO']
					y = orbital_cont(proc_name)
					dic_exc = {'Oscillator Force' : y[0],'Wavelength' : y[1]}
					single_list_number = 1
					for single_list in y[2]:
						list_number_ID = single_list_number - 1
						dic_exc['Orbital Source %s' %(single_list_number)] = ((y[2])[list_number_ID])[0]
						dic_exc['Target Orbital %s' %(single_list_number)] = ((y[2])[list_number_ID])[1]
						dic_exc['Contribution %s' %(single_list_number)] = 200*float(((y[2])[list_number_ID])[2])*float(((y[2])[list_number_ID])[2])
						single_list_number=1+single_list_number
					print_values()
					contrib_values()

			if state_dir is 'otimizacao':
				os.chdir(work_dir+'/'+state_dir+'/'+solvent)
				proc_name = 'bsd_'+molecule+'_opt_S0'
				dipoles = []
				dipole_moment = dipole_process(proc_name)
				occ_orbitals = []
				virtual_orbitals = []
				orbitals = orbital_process(proc_name)
				bandgap = orbitals['LUMO'] - orbitals['HOMO']
				print_values()

result_file.close()

