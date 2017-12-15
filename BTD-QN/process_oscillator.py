__author__ = "Thiago Lopes"
import os
from find_a_string_in_file import Find_a_String

base_name = "BTD-QN"
solvents = {"gas":" ", "water":"scrf=(iefpcm, solvent=Water)"}
methods = ["B3LYP", "CAM-B3LYP", "M062X", "PBE1PBE", "wB97XD"]
lookup = " Excited State  "
nstates=12
dir_home = os.getcwd()
wl_exp = 445

for solvent in list(solvents.keys()):
    primer_transitions_wl = []
    exp_ref = []
    processed_file = open(dir_home+"/"+solvent+"/"+solvent+"_uv_scpectra_g09.txt", "w")
    for method in methods:
        states = []
        states_1 = -1
        states_2 = 0
        fileLogName = dir_home+"/"+solvent+"/"+base_name+"_"+solvent+"_"+method+".log"
        lines = Find_a_String(fileLogName, lookup).return_numbers_of_line()
        with open(fileLogName) as myFile:
            for num, line in enumerate(myFile):
                if num in range(lines[0]-1, lines[-1]+15, 1):
                    if (num+1) in lines:
                        states.append([line.strip(), []])
                        states_1 +=1
                    try:
                        if line.split()[1] == "->":
                            states[states_1][1].append(line.strip())
                    except:
                        pass
        wavelength_list = []
        for state in states:
            wavelength = float(state[0].split()[6])
            wavelength_list.append(wavelength)
        max_wl = max(wavelength_list)
        principal_transition = wavelength_list.index(max_wl)
        primer_transitions_wl.append(max_wl)
        processed_file.write(base_name+"_"+solvent+"_"+method+".log\n")
        exp_ref.append(abs(max_wl-wl_exp))

        processed_file.write("Principal Transition: {}{:10s}Wave-lenght:{}\n\n".format(principal_transition+1, "", wavelength_list[principal_transition]))
        for state in states:
            processed_file.write(state[0]+"\n")
            for transition in state[1]:
                processed_file.write(transition+"\n")
            processed_file.write("\n")
        processed_file.write("\n")
        min_dif = min(exp_ref)
        minimal_dif = exp_ref.index(min_dif)
    count = 0
    processed_file.write("Summary:\n\n")
    for method in methods:
        processed_file.write("{:3s}{:10s} Best transition in {} nm\n".format("",method+" - ", primer_transitions_wl[count]))
        processed_file.write("{:14s}{:.2f} nm from experimental data (water)\n\n".format("",exp_ref[count]))
        count+=1
    processed_file.write("The functional with the main transition closer to the experimental one was: {}\n" .format(methods[minimal_dif]))