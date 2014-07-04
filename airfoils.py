#!/usr/bin/env python

'''
manipulate airfoil data and write it to new text file that can be used in solidworks
'''

import numpy as np
from matplotlib.pyplot import *
import argparse

class airfoil(object):

    def __init__(self, data_in):
        self.data_in = data_in

    def scale(self, x):
        with open(self.data_in) as input_file:
            data_lists = []
            for line in input_file:
                data_lists.append(line.strip().split())
        scaled_lists = []
        for lst in data_lists:
            scaled_list = []
            for i in lst:
                scaled_i = float(i) * x
                scaled_list.append(scaled_i)
            scaled_lists.append(scaled_list)
        return scaled_lists    

    def write_new(self, x=1.0):
        filename = self.data_in[:-4] + "_S%s.txt" % x
        new_file = open(filename, 'w')
        scaled_lists = self.scale(x)
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

    def fix_data(self, n, x=1.0):
        scaled_lists = self.scale(x)
        x_list = []
        y_list = []
        for pair in scaled_lists:
            x_list.append(pair[0])
            y_list.append(pair[1])
        x_array = np.asarray(x_list)
        y_array = np.asarray(y_list)
        if fix >= 1:
            #this option creates shitty data at the moment. working on it!
            for i in range(len(x_array)):
                if x_array[i] == y_array[i]:
                    stop = i
                    print stop
                    print x_array[i]
                    break
            px_array = x_array[:stop+1]
            py_array = y_array[:stop+1]
            nx_array = x_array[stop:]
            ny_array = y_array[stop:]
            p_coeffs = np.polyfit(px_array, py_array, n)
            n_coeffs = np.polyfit(nx_array, ny_array, n)
            py_poly = np.poly1d(p_coeffs)
            ny_poly = np.poly1d(n_coeffs)
            px_fixed = np.linspace(min(px_array), max(px_array), 100)
            py_fixed = py_poly(px_fixed)
            nx_fixed = np.linspace(min(nx_array), max(nx_array), 100)
            ny_fixed = ny_poly(nx_fixed)
            print nx_fixed
            print ny_fixed
            x_fixed = np.concatenate([px_fixed, nx_fixed])
            y_fixed = np.concatenate([py_fixed, ny_fixed])
            return x_fixed, y_fixed
        else:
            return x_array, y_array

    def plot_data(self, n, x=1.0):
        x_array, y_array = self.fix_data(n, x)
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
            help = "must be .txt format containing x and y data columns. if data contains third column for z coordinates, it will be ignored and replaced with zeros. any whitespace between data points is used to split the data and eliminated"
            )
    parser.add_argument("-f", "--fix",
            action = "store",
            type = int,
            help = "attempts to fix data with too few data points with a polyfit"
            )
    parser.add_argument("-w", "--write",
            action = "store_true",
            help = "writes manipulated data to new file with automated filename. overwrites existing filename if it exists already. see README.md for examples"
            )
    parser.add_argument("-s", "--scale",
            action = "store",
            type = float,
            help = "float type, scales the data to data * s"
            )
    
    parser.add_argument("-p","--plot",
            action = "store_true",
            help = "plots the scaled data. if data_out given, new file will still be written"
            )
    args = parser.parse_args()
    
    new_airfoil = airfoil(args.data_in)

    if args.fix:
        fix = args.fix
    else:
        fix = 0
    
    if args.write:
        if args.scale and args.plot:
            new_airfoil.write_new(args.scale)
            new_airfoil.plot_data(fix, args.scale)
        elif args.scale:
            new_airfoil.write_new(args.scale)
        elif args.plot:
            new_airfoil.plot_data(fix)
        else:
            new_airfoil.write_new()
    elif args.plot:
        if args.scale:
            new_airfoil.plot_data(fix, args.scale)
        else:
            new_airfoil.plot_data(fix)
    else:
        print "Not enough input arguments. Use --help option for required inputs"


