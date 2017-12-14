import os
from find_xyz_from_a_log import Find_XYZ

base_name = "BTD-QN"

solvents = {"gas":" ", "water":"scrf=(iefpcm, solvent=Water)"}
methods = ["B3LYP", "CAM-B3LYP", "M062X", "PBE1PBE", "wB97XD"]
td_text = "td=nstates=12"
basis_set = "6-311+G(2d,p)"
text_add_work = "density=current NoSymm"
proc_line = "%nprocshared=6"
mem_line = "%mem=30000MB"
mult = "1"
charge = "0"
text_base = "Calculo TD da "
dir_home = os.getcwd()

for solvent in list(solvents.keys()):
    geom_orig = dir_home+"/opt/"+base_name+"_"+solvent+".log"
    geom_list = Find_XYZ(geom_orig, 30).gaussian_style()
    os.chdir(dir_home+"/"+solvent)
    for method in methods:
        checkpoint_line = "%chk="+base_name+"_"+solvent+"_"+method+".chk"
        file_name=base_name+"_"+solvent+"_"+method+".com"
        text = text_base+file_name
        file_to_write = open(file_name, "w")
        file_to_write.write("{}\n{}\n{}\n".format(checkpoint_line, mem_line, proc_line))
        file_to_write.write("#p {}/{} {} {} {}\n\n{}\n\n{} {}\n".format(method, basis_set, td_text, text_add_work, solvents[solvent], text, charge, mult))
        for element in geom_list:
            file_to_write.write("{}\n".format(element))
        file_to_write.write("\n\n")
    