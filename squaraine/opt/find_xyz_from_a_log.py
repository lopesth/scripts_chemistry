__author__ = "Thiago Lopes"
__email__ = "lopes.th.o@gmail.com"
__date__ = "Nov 17 of 2017"

from find_a_string_in_file import Find_a_String
from periodic_table import Convert_Period_Table

class Find_XYZ(object):

    def __init__(self, file, base):
        self.file = file
        self.base = base

    def stop_the_pigeon(self):
        self.temp_list = []
        pos_start = Find_a_String(self.file, "Input orientation").return_numbers_of_line()[-1] + 5
        pos = range(pos_start, pos_start + self.base)
        with open(self.file) as myFile:
            for num, line in enumerate(myFile, 1):
                if (num in pos):
                    self.temp_list.append(line.split())
        return self.temp_list

    def gaussian_style(self):
        self.stop_the_pigeon()
        final_list = []
        for line in self.temp_list:
            atomic_symbol = Convert_Period_Table([int(line[1])], []).number_to_symbol()
            final_list.append("{:>2s} {:>13.7f} {:>13.7f} {:>13.7f}".format(atomic_symbol[0], float(line[3]), float(line[4]), float(line[5])))
        return final_list
