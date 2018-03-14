#########################################################################################
# Python file header
__author__ = "Thiago Lopes"
__GitHubPage__ = "https://github.com/lopesth"
__email__ = "lopes.th.o@gmail.com"
__date__ = "Friday, 12 January 2018"

''' Description: Find a specific string in a file'''
#########################################################################################

class Find_a_String(object):

    def __init__(self, file, lookup):
        self.file = file
        self.lookup = lookup

    def return_numbers_of_line(self):
        numbers = []
        myFileString = []
        with open(self.file) as myFile:
            for num, line in enumerate(myFile):
                if (self.lookup in line):
                    numbers.append(num+1)
        return numbers

    def return_the_line(self):
        lines = []
        with open(self.file) as myFile:
            for num, line in enumerate(myFile):
                if (self.lookup in line):
                    lines.append(line.split('\n')[0])
        return lines
