__author__ = "Thiago Lopes"
__email__ = "lopes.th.o@gmail.com"
__date__ = "Dec 15 of 2017"
import os 
from find_xyz_from_a_log import Find_XYZ

base_name = "BTD-QN"
solvents = {"gas":" ", "water":""}
methods = ["B3LYP", "CAM-B3LYP", "M062X", "PBE1PBE", "wB97XD"]
base = 30
dir_home = os.getcwd()
all_geom_file = open(dir_home+"/"+"allGeomFile.dat", "w")
for solvent in list(solvents.keys()):
    all_geom_file.write(" In {} fase\n\n".format(solvent))
    for method in methods:
        geom_orig = dir_home+"/"+solvent+"/"+base_name+"_"+solvent+"_"+method+".log"
        geom_list = Find_XYZ(geom_orig, 30).gaussian_style()
    for line in geom_list:
        all_geom_file.write("{}\n".format(line))
    all_geom_file.write("\n")





