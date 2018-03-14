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
from find_a_string_in_file import Find_a_String
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

# Function Description: Function to Separate the CPs from head e footer of AIMALL file
def separateAIMALLfile(fileName):
    listofCPs = Find_a_String(listToDo[0] , "CP# ").return_numbers_of_line()
    listofCPs.append(Find_a_String(listToDo[0] , "Number of ").return_numbers_of_line()[0])
    file = open(fileName, "r")
    fileINlist = []
    for line in file:
        fileINlist.append(line.split('\n')[0])
    fileLISThead = fileINlist[0:listofCPs[0]-1]
    fileLISTfooter = fileINlist[listofCPs[-1]:]
    fileLISTCPs = fileINlist[listofCPs[0]:listofCPs[-1]-1]
    return[fileLISThead, fileLISTCPs, fileLISTfooter]

# Function Description: Function to remove the a certain type of CCPs
def removeCPsTypes(fileLISTCPs, CPtypetoREMOVE):
    print(CPtypetoREMOVE)
    listofCPs = []
    fileLISTCPsnew = []
    number = 0
    for element in fileLISTCPs:
        if "CP# " in element:
            listofCPs.append(number)
        number += 1
    gettedCPs = []
    anchor = 0
    for element in range(0, len(listofCPs)-1):
        if CPtypetoREMOVE in fileLISTCPs[int(listofCPs[element])+1]:
            startPOS = int(listofCPs[element])
            for x in fileLISTCPs[anchor:startPOS]:
                fileLISTCPsnew.append(x)
            anchor = int(listofCPs[element+1])  
    return fileLISTCPsnew

P# Function Description: Function to remove the CPs of Selection Atons
def removeAtomCPs(CPsList, atonsList):
    print("")

# Function Description: Remove selected CPs
def removeCPs(listToDo):
    fileLISThead, fileLISTCPs, fileLISTfooter = separateAIMALLfile(listToDo[0])
    if listToDo[1] == True:
        fileLISTCPs = removeCPsTypes(fileLISTCPs, "RCP")
    if listToDo[2] == True:
        fileLISTCPs = removeCPsTypes(fileLISTCPs, "CCP")
    if len(listToDo[3]) > 0:
        fileLISTCPs =  removeAtomCPs(fileLISTCPs, listToDo[3])
    


# Description: main function of the script
if (__name__ == "__main__"):
    listToDo = readInputFile(sys.argv[1])
    removeCPs(listToDo)
    

