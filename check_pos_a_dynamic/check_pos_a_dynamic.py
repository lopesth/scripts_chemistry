#########################################################################################

__author__ = "Thiago Lopes"
__GitHubPage__ = "https://github.com/lopesth"
__email__ = "lopes.th.o@gmail.com"
__date__ = "Jan 03 of 2018"

# Description: 

######################################################################################## 

iso_file_name = "pos1_isol_epinefrina.geom"  # only atom and xyz in file
box_file_name = "pos1_din_epinefrina.geom"   # only atom and xyz in file

def transformFileinList(file):
	list_t = []
	with open(file) as myFile:
		for line in myFile:
			x = line.split()
			y = [x[0], float(x[1]), float(x[2]), float(x[3])]
			list_t.append(y)
	return list_t

def compareAtonsPos(atom1, atom2):
	if (atom1[0] == atom2[0]):
		if (atom1[1] == atom2[1]):
			if (atom1[2] == atom2[2]):
				if (atom1[3] == atom2[3]):
					return True
	return False


iso_list = transformFileinList(iso_file_name)
box_list = transformFileinList(box_file_name)
posList = []

for atomAnchor in range(0, len(iso_list), 1):
	boxAnchor = 0
	pause = False
	while not pause:
		pause = compareAtonsPos(iso_list[atomAnchor], box_list[boxAnchor])
		if (pause == True):
			posList.append(boxAnchor+1)
		boxAnchor +=1

print(posList)