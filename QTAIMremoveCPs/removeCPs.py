 #########################################################################################
# Python file header
__author__ = "Thiago Lopes"
__GitHubPage__ = "https://github.com/lopesth"
__email__ = "lopes.th.o@gmail.com"
__date__ = "Monday, 12 March 2018"

''' Description: Script to remove CPs in AIMALL's output'''
#########################################################################################

#########################################################################################
# Impoted Modules
import sys
#########################################################################################

# Function Description:  Function for read the input file
def readInputFile(fileName):
    inputFile = open(fileName, "r")
    input = []
    for line in inputFile:
        if len(line.strip()) > 0:
            input.append(line.split('\n')[0])
    filePath = input[1].strip()
    try:
        f = open(filePath, "r")
        f.close()
    except:
        print("There is no file in indicated path")
        exit(0)
    aswRCP = yesORno(input[3])
    if aswRCP == "Error":
        print("Error in Answer of Question: 'Remove RCP?'")
        exit(0)
    aswCCP = yesORno(input[5])
    if aswCCP == "Error":
        print("Error in Answer of Question: 'Remove RCP?'")
        exit(0)
    atonsList = input[7:]
    return([filePath, aswRCP, aswCCP, atonsList])

# Function Description: Find the answer Yes or No
def yesORno(list):
    output = []
    resp1 = list.split("(")
    for element in resp1:
        if len(element) > 0:
            resp2 = element.split(")")
            for element2 in resp2:
                output.append(element2)
    if output[0] == 'X' or output[0] == 'x':
        return True
    if output[2] == 'X' or output[2] == 'x':
        return False
    else:
        return "Error"

# Function Description: Function to remove the RCPs
def removeRCPs(trueORfalse, fileName):
    filetoRead = open(fileName, "r")
    filetoWrite = open(fileName.split(".mgpviz")[0]+"_temp1.mgpviz", "w")
    filetoWrite.write("/n")

# Function Description: Function to remove the CCPs
def removeCCPs(trueORfalse, fileName):
    filetoRead = open(fileName, "r")
    filetoWrite = open(fileName.split("_temp1.mgpviz")[0]+"_temp2.mgpviz", "w")
    filetoWrite.write("/n")

# Function Description: Remove selected CPs
def removeCPs(listToDo):
    removeRCPs(listToDo[1], listToDo[0])
    removeCCPs(listToDo[2], listToDo[0].split(".mgpviz")[0]+"_temp1.mgpviz")

# Description: main function of the script
if (__name__ == "__main__"):
    listToDo = readInputFile(sys.argv[1])
    removeCPs(listToDo)
    

