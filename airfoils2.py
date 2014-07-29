#!/usr/bin/env python

'''
manipulate existing airfoil data and write it to new text file that can be used in solidworks
'''

import numpy as np
from matplotlib.pyplot import *
import argparse
import re

class airfoil(object):

    def __init__(self, data_in):
        self.data_in = data_in

    def scale(self, x, opt=False):
        with open(self.data_in) as input_file:
            data_lists = []
            for line in input_file:
                if re.search("[a-zA-Z]", line) == None and re.search("[0-9]", line):
                    data_lists.append(line.strip().split())
            if opt == True:
                chord_pair = data_lists[0]
                chord = float(chord_pair[0])
                x = x / chord
        scaled_lists = []
        for lst in data_lists:
            scaled_list = []
            for i in lst:
                scaled_i = float(i) * x
                scaled_list.append(scaled_i)
            scaled_lists.append(scaled_list)
        return scaled_lists    

    def write_new(self, x=1.0, opt=False):
        filename = self.data_in[:-4] + "_%s.txt" % x
        new_file = open(filename, 'w')
        scaled_lists = self.scale(x, opt)
        for lst in scaled_lists:
            string_pair = ""
            for i in lst:
                as_string = str(float(i))
                string_pair += as_string + '  '
            if len(lst) == 2:
                string_pair += '0.0'
            else:
                string_pair = string_pair[:-2]
            new_file.write(string_pair + '\n')
        new_file.close()

    def fix_data(self, x=1.0, opt=False):
        scaled_lists = self.scale(x, opt)
        x_list = []
        y_list = []
        for pair in scaled_lists:
            x_list.append(pair[0])
            y_list.append(pair[1])
        x_array = np.asarray(x_list)
        y_array = np.asarray(y_list)
        return x_array, y_array

    def get_specs(self, x=1.0, opt=False):
        x_array, y_array = self.fix_data(x, opt)
        for index in range(len(x_array)):
            if x_array[index] == 0.0:
                if index != 0:
                    switch = index
        if len(x_array) % 2 == 0:
            y_upper = y_array[:switch]
            y_lower = y_array[switch:]
        else:
            y_upper = y_array[:switch]
            y_lower = y_array[switch+1:][::-1]
        chord = max(x_array)
        camber = abs(abs(y_upper) - abs(y_lower))
        max_camb = max(camber)
        pos_camb = x_array[np.where(camber == max_camb)][0]
        thickness = max(abs(y_upper) + abs(y_lower))
        return camber, switch, max_camb*100, pos_camb*100, thickness*100

    def plot_data(self, x=1.0, opt=False):
        camber, switch, a,b,c = self.get_specs(x, opt)
        x_array, y_array = self.fix_data(x, opt)
        plot(x_array[:switch], camber)
        plot(x_array, y_array, linestyle="-")
        xlabel("x coordinates, any units")
        ylabel("y coordinates, any units")
        grid(True)
        lim = max(x_array) + .03
        xlim(-.03, lim)
        ylim(-lim/2, lim/2)
        suptitle("Scaled airfoil plot", fontsize=20)
        show()


if __name__=="__main__":

    parser = argparse.ArgumentParser(
            description = "Takes common airfoil data format and manipulates it as specified by arguments"
            )
    parser.add_argument("data_in",
            type = str,
            help = "must be plain text format (.txt, .md, etc) containing x and y data columns. if data contains third column for z coordinates, it will be ignored and replaced with zeros. any whitespace between data points is used to split the data and eliminated"
            )
    
    parser.add_argument("-w", "--write",
            action = "store_true",
            help = "writes manipulated data to new file with automated filename (adds an extention with the scaling factor). overwrites existing filename if it exists already. see README.md for examples"
            )
    parser.add_argument("-s", "--scale",
            action = "store",
            type = float,
            help = "float type, scales the data to data * s"
            )
    parser.add_argument("-o", "--optimal",
            action = "store_true",
            help = "default False, True if selected. turns --scale argument into the maximum chord length"
            )
    parser.add_argument("-p","--plot",
            action = "store_true",
            help = "plots the scaled data"
            )
    parser.add_argument("-k", "--keyInfo",
            action = "store_true",
            help = "returns max camber, max camber position, and thickness of the airfoil. useful if the data you have is kinda bad/doesn't have enough data points for a smooth curve, etc. you can then plug the results into makefoil.py to get an airfoil with these parameters with desired number of data points/scaling"
            )
    args = parser.parse_args()
    
    new_airfoil = airfoil(args.data_in)

    if args.optimal:
        opt_cond = True
    else:
        opt_cond = False

    def get_keyInfo():
        a,b, max_camb, pos_camb, thickness = new_airfoil.get_specs()
        print "max camber: %s%%"% max_camb
        print "position of max camber: %s%%" % pos_camb
        print "thickness of airfoil: %s%%" % thickness

    if args.write:
        if args.scale and args.plot and args.keyInfo:
            new_airfoil.write_new(args.scale, opt_cond)
            new_airfoil.plot_data(args.scale, opt_cond)
            get_keyInfo()
        elif args.scale and args.keyInfo:
            new_airfoil.write_new(args.scale, opt_cond)
            get_key_info()
        elif args.plot and args.keyInfo:
            new_airfoil.plot_data()
            new_airfoil.write_new()
            get_keyinfo()
        elif args.plot:
            new_airfoil.plot_data()
        elif args.keyInfo:
            get_keyInfo()
        else:
            new_airfoil.write_new()
    elif args.plot:
        if args.scale and args.keyInfo:
            new_airfoil.plot_data(args.scale, opt_cond)
            get_keyInfo()
        elif args.keyInfo:
            new_airfoil.plot_data()
            get_keyInfo()
        else:
            new_airfoil.plot_data()
    else:
        print "Not enough input arguments. Use --help option for required inputs"


