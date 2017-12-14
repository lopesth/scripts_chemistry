#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""

Python 2.7

Created on Thu, 02 March  09:32h BRST 2017

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Program to process Gabi`s CEPs

"""

import numpy, os, itertools
import matplotlib.pyplot as plt

def lookup_in_file(file_to_open, lookup_string):
	with open(file_to_open) as myFile:
		for line in myFile:
			if lookup_string in line:
				return line

models = ["1","2","3","4"]
isolated_molecules = ['fulerene', 'pentacene']
pcm_status_list = ["solvent", "vaccum"]
pwd_command = 'pwd'
folder_home = os.popen(pwd_command, 'r', 1).read().split()[0]

folder_target_molecules_g09outputs = folder_home+'/moleculas_isoladas/arquivos_output'
reference_withoutGrimme = {}
reference_withGrimme = {}

os.chdir(folder_target_molecules_g09outputs)
for molecule in isolated_molecules:
	for pcm_status in pcm_status_list:
		energy_molecule_found = float(lookup_in_file(molecule+"_"+pcm_status+".log", "SCF Done:").split()[4])
		gd3_molecule_found = float(lookup_in_file(molecule+"_"+pcm_status+".log", "Grimme-D3 Dispersion energy").split()[4])
		
		if molecule == "fulerene" and pcm_status == "solvent":
			reference_withoutGrimme.update({"fulerene_solvent" : energy_molecule_found})
			reference_withGrimme.update({"fulerene_solvent" : energy_molecule_found+gd3_molecule_found})
		if molecule == "fulerene" and pcm_status == "vaccum":
			reference_withoutGrimme.update({"fulerene_vaccum" : energy_molecule_found})
			reference_withGrimme.update({"fulerene_vaccum" : energy_molecule_found+gd3_molecule_found})
		if molecule == "pentacene" and pcm_status == "solvent":
			reference_withoutGrimme.update({"pentacene_solvent" : energy_molecule_found})
			reference_withGrimme.update({"pentacene_solvent" : energy_molecule_found+gd3_molecule_found})
		if molecule == "pentacene" and pcm_status == "vaccum":
			reference_withoutGrimme.update({"pentacene_vaccum" : energy_molecule_found})
			reference_withGrimme.update({"pentacene_vaccum" : energy_molecule_found+gd3_molecule_found})

for NameModel in models:
	folder_target_complex_g09outputs = folder_home+'/model'+NameModel+'/aquivos_output/'

	os.chdir(folder_target_complex_g09outputs)
	
	if NameModel == "1" or NameModel == "2":
		increments = numpy.arange(4.0, 9.6, 0.1)
	if NameModel == "3" or NameModel == "4":
		increments = numpy.arange(11.0, 16.7, 0.1)
		
	for pcm_status in pcm_status_list:
		energy_complex_withGrimme_all = []
		energy_complex_withGrimme_complex = []
		energy_complex_withoutGrimme = []
		output_withGrimme_all = open(folder_home+'/model'+NameModel+'_'+pcm_status+'_with_Grimme_complexOnly.processed' , 'w', 1)
		output_withGrimme_complex = open(folder_home+'/model'+NameModel+'_'+pcm_status+'_with_Grimme_all.processed' , 'w', 1)
		output_withoutGrime = open(folder_home+'/model'+NameModel+'_'+pcm_status+'_without_Grimme.processed' , 'w', 1)
		
		for increment in increments:
			outputFileName = "model"+str(NameModel)+"_"+str(increment)+"_"+str(pcm_status)
			energy_found = float(lookup_in_file(outputFileName+".log", "SCF Done:").split()[4])
			gd3_found = float(lookup_in_file(outputFileName+".log", "Grimme-D3 Dispersion energy").split()[4])
			
			if pcm_status == "solvent":
				
				energy_complex_withGrimme_all.append(
					energy_found + gd3_found - (reference_withGrimme['fulerene_solvent'] + reference_withGrimme['pentacene_solvent'])
				)
				
				energy_complex_withGrimme_complex.append(
					energy_found + gd3_found - (reference_withGrimme['fulerene_solvent'] + reference_withoutGrimme['pentacene_solvent'])
				)
				
				energy_complex_withoutGrimme.append(
					energy_found - (reference_withoutGrimme['fulerene_solvent'] + reference_withoutGrimme['pentacene_solvent'])
				)
				
			if pcm_status == "vaccum":
				
				energy_complex_withGrimme_all.append(
					energy_found + gd3_found - (reference_withGrimme['fulerene_vaccum'] + reference_withGrimme['pentacene_vaccum'])
				)

				energy_complex_withGrimme_complex.append(
					energy_found + gd3_found - (reference_withGrimme['fulerene_solvent'] + reference_withoutGrimme['pentacene_solvent'])
				)

				energy_complex_withoutGrimme.append(
					energy_found - (reference_withoutGrimme['fulerene_vaccum'] + reference_withoutGrimme['pentacene_vaccum'])
				)
				

				
		for list_element, increment in itertools.izip(range(0,len(energy_complex_withGrimme_all)), increments):
			output_withGrimme_all.write( "%-15.7f	%15.10f\n"   %(float(increment) * 1.889725989,energy_complex_withGrimme_all[list_element] - energy_complex_withGrimme_all[-1]))
			
		for list_element, increment in itertools.izip(range(0,len(energy_complex_withGrimme_all)), increments):
			output_withGrimme_complex.write( "%-15.10f	%15.7f\n"   %(float(increment) * 1.889725989,energy_complex_withGrimme_complex[list_element] - energy_complex_withGrimme_complex[-1]))	
			
		for list_element, increment in itertools.izip(range(0,len(energy_complex_withoutGrimme)), increments):
			output_withoutGrime.write("%-15.7f	%15.10f\n"   %(float(increment) * 1.889725989,energy_complex_withoutGrimme[list_element] - energy_complex_withoutGrimme[-1]))



