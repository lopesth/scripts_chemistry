# -*- coding: UTF-8 -*-


def cataloga_atomos(file_input):
	lista_atomos = []
	with open(file_input) as myFile:
		for num, line in enumerate(myFile, 1):
			if "HETATM" in line:
				if line.split()[2] in lista_atomos:
					pass
				else:
					lista_atomos.append(line.split()[2])
	return lista_atomos
def separa_atomos(file_input, lista_atomos):
	atomos_separados = []
	linhas_arquivo = []
	linhas_atomos = []
	with open(file_input) as myFile:
		for line in myFile:
			linhas_arquivo.append(line.split())
	for linha in linhas_arquivo:
		if len(linha) > 5:
				if linha[3] == "A":
					x = [linha[2], linha[5], linha[6], linha[7]]
					linhas_atomos.append(x)
				else:
					x = [linha[2], linha[4], linha[5], linha[6]]
					linhas_atomos.append(x)
	for atomo in lista_atomos:
		lista_atomo = []
		for linha_atomo in linhas_atomos:
			if atomo == linha_atomo[0]:
				lista_atomo.append(linha_atomo)
		atomos_separados.append(lista_atomo)
	return atomos_separados


file_inputs = {"meroc_clorof":["merocyanine_clorof_box.pdb", "21.51",["C_VDB_PBE", "Cl_VDB_PBE", "H_VDB_PBE", "N_VDB_PBE", "O_VDB_PBE"]], "meroc_water" : ["merocyanine_water_box.pdb", "15.82", ["C_VDB_PBE", "Cl_VDB_PBE", "H_VDB_PBE", "N_VDB_PBE", "O_VDB_PBE"]]}
lmax_list = {"N" : "LMAX=P", "H" : "LMAX=S", "Cl" : "LMAX=P", "C" : "LMAX=P", "O" : "LMAX=P"}
for molecule in file_inputs.keys():
	file_input = file_inputs[molecule][0]
	cell = file_inputs[molecule][1]
	files_psp = file_inputs[molecule][2]
	lista_de_atomos = cataloga_atomos(file_input)
	lista_atomos_separados = separa_atomos(file_input, lista_de_atomos)
	file_wf= open(molecule + "_WF.inp", "w", 1)
	file_dyn = open(molecule + "_Dyn.inp", "w", 1)
	file_wf.write("&INFO\n  Minimização da Função de Onda do %s\n\n&END\n\n" %(molecule))
	file_dyn.write("&INFO\n Dinamica do %s\n\n&END\n\n" %(molecule))
	file_wf.write("&CPMD\n\n LSD\n OPTIMIZE WAVEFUNCTION\n CONVERGENCE ORBITALS\n  1.0d-7\n CENTER MOLECULE ON\n PRINT FORCES ON\n MEMORY BIG\n\n SPLINE POINTS\n 2000\n ODIIS\n  10\n\n&END\n\n")
	file_dyn.write("&CPMD\n\n LSD\n MOLECULAR DYNAMICS CP\n RESTART WAVEFUNCTION COORDINATES VELOCITIES NOSEE NOSEP LATEST\n PRINT FORCES ON\n MEMORY BIG\n\n  TRAJECTORY SAMPLE XYZ\n\n  5\n  RESTFILE\n  1\n\n  MAXSTEP\n  100000\n\n  TIMESTEP\n  2.0\n\n  NOSE IONS MASSIVE\n  300.0 1600.0\n\n  NOSE ELECTRONS\n  0.007 15000.0\n\n  NOSE PARAMETERS\n  3 3 3 6.0D0 15 4\n  SUBTRACT COMVEL ROTVEL\n  100\n\n&END\n\n")
	file_wf.write("&DFT\n OLDCODE\n FUNCTIONAL PBE\n&END\n\n")
	file_dyn.write("&DFT\n OLDCODE\n FUNCTIONAL PBE\n&END\n\n")
	file_wf.write("&SYSTEM\n MULTIPLICITY\n  1\n CHARGE\n  0\n SYMMETRY\n  1\n ANGSTROM\n CELL\n  %s 1.0 1.0  0.0  0.0  0.0\n\n CUTOFF\n  25.0\n\n DUAL\n  4.0\n&END\n\n" %(cell))
	file_dyn.write("&SYSTEM\n MULTIPLICITY\n  1\n CHARGE\n  0\n SYMMETRY\n  1\n ANGSTROM\n CELL\n  %s 1.0 1.0  0.0  0.0  0.0\n\n CUTOFF\n  25.0\n\n DUAL\n  4.0\n&END\n\n" %(cell))
	file_wf.write("&ATOMS\n")
	file_dyn.write("&ATOMS\n")
	for atomo in lista_atomos_separados:
		number_of_atom = len(atomo)
		atom_name = (atomo[0])[0]
		for psp in file_inputs[molecule][2]:
			if atom_name == psp.split("_")[0]:
					file_wf.write("*%s.psp FORMATTED\n %s\n %d\n" %(psp, lmax_list[atom_name], number_of_atom))
					file_dyn.write("*%s.psp FORMATTED\n %s\n %d\n" %(psp, lmax_list[atom_name], number_of_atom))
					for atom_xyz in atomo:
						file_wf.write("      %8.5f %8.5f %8.5f\n" %(float(atom_xyz[1]), float(atom_xyz[2]), float(atom_xyz[3])))
						file_dyn.write("      %8.5f %8.5f %8.5f\n" %(float(atom_xyz[1]), float(atom_xyz[2]), float(atom_xyz[3])))
	
					file_wf.write("\n")
					file_dyn.write("\n")

	file_wf.write("&END\n\n")
	file_dyn.write("&END\n\n")














