#!/usr/bin/env python

'''
manipulate airfoil data and write it to new text file that can be used in solidworks
'''
import numpy as np
from matplotlib.pyplot import *
import argparse

#takes airfoil data, scales it, and returns it as a list of "x y" paired strings
def scale_airfoil(data_in, x):
    with open(data_in) as input_file:
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

def write_data(data_in, data_out, x):
    data_file = open(data_out, 'w')
    scaled_lists = scale_airfoil(data_in, x)
    for lst in scaled_lists:
        string_pair = ""
        for i in lst:
            as_string = str(float(i))
            string_pair += as_string + '  '
        if len(lst) == 2:
            string_pair += '0.0'
        else:
            string_pair -= '  '
        data_file.write(string_pair + '\n')
    data_file.close()

def plot_data(data_in, x):
    scaled_lists = scale_airfoil(data_in, x)
    x_list = []
    y_list = []
    error = scaled_lists[17]
    for pair in scaled_lists:
        x_list.append(pair[0])
        y_list.append(pair[1])
    x_array = np.asarray(x_list)
    y_array = np.asarray(y_list)
    plot(x_array, y_array, linestyle="-")
    xlabel("x coordinates, any units")
    ylabel("y coordinates, any units")
    grid(True)
    lim = max(x_array)
    xlim(0, lim)
    ylim(-lim/2, lim/2)
    suptitle("Scaled airfoil plot", fontsize=20)
    show()


if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Takes x and y data columns (sparated by commas) for airfoil curves and scales and writes them to new text file in solidworks compatible format")
    parser.add_argument("data_in", type=str, help="must be .txt format containing x and y data columns. if data contains third column for z coordinates, it will be ignored and replaced with zeros. any whitespace between data points is used to split the data and eliminated")
    parser.add_argument("x", type=float, help="float type, scales the data to data * x")
    parser.add_argument("data_out", nargs="?", type=str, help="filename to write processed data to. must be .txt format")
    parser.add_argument("-p", "--plot", action="store_true", help="plots the scaled data. if data_out given, new file will still be written")
    args = parser.parse_args()

    if args.data_out:
        if args.plot:
            plot_data(args.data_in, args.x)
        write_data(args.data_in, args.data_out, args.x)
    else:
        if args.plot:
            plot_data(args.data_in, args.x)
        else:
            print "Not enough inputs given. try --help for more information."

