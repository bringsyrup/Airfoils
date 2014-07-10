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

    def scale(self, s, n):
        data_arrays = np.loadtxt(self.data_in, dtype=float)
        x_array = []
        y_array = []
        for pair in data_arrays:
            x_array.append(pair[0])
            y_array.append(pair[1])
        if n > 0:
            yU_data = []
            yL_data = []
            for num in y_array:
                if num > 0.:
                    yU_data.insert(0, num)
                elif num < 0.:
                    yL_data.append(num)
            c = max(x_array)                            # chord length
            t = (max(y_array) - min(y_array)) / c       # max thickness
            m = float(self.data_in[-8]) / 100.          # max camber as % of c
            p = float(self.data_in[-7]) / 10.           # position of m as % of c
            x = np.linspace(0, c, n)                    # range of x position
            show()
            a_o = 0.2969                                # coefficients found by NACA
            a_1 = -0.1260
            a_2 = -0.3516
            a_3 = 0.2843
            a_4 = -0.1036
            y_t = t*c/.2 * (a_o*np.sqrt(x/c) + a_1*x/c + a_2*np.power((x/c), 2) + a_3*np.power((x/c), 3) + a_4*np.power((x/c), 4))
            y_cr = m*x[0:p*c]/pow(p, 2) * (2*p - x[0:p*c]/c)
            y_cf = m*(c-x[p*c:])/pow(1-p, 2) * (1+x[p*c:]/c-2*p)
            theta_r = np.arctan(2*m/pow(p, 2) * (p-x[0:p*c]/c))
            theta_f = np.arctan(2*m/pow(1-p, 2) * (p-x[p*c:]/c))
            y_c = np.concatenate([y_cr, y_cf])            
            theta = np.concatenate([theta_r, theta_f])
            xU = np.asarray(x - y_t*np.sin(theta))
            xL = np.asarray(x + y_t*np.sin(theta))
            yU = np.asarray(y_c + y_t*np.cos(theta))
            yL = np.asarray(y_c - y_t*np.cos(theta))
            x_fixed = np.concatenate([xU, xL[::-1]])
            y_fixed = np.concatenate([yU, yL[::-1]])
            x_array = x_fixed * s
            y_array = y_fixed * s
        else:
            x_array = x_array * s
            y_array = y_array * s
        return x_array, y_array

    def write_new(self, s=1.0, n=0):
        filename = self.data_in[:-4] + "_S%s.txt" % s
        new_file = open(filename, 'w')
        x_array, y_array = self.scale(s, n)
        #scaled_arrays = self.scale(x, n)
        for i in range(len(x_array)):
            string_pair = str(x_array[i]) + " " + str(y_array[i]) + " " "0.0"
            new_file.write(string_pair + "\n")
        new_file.close()

    def plot_data(self, s=1.0, n=0):
        x_array, y_array = self.scale(s, n)
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
    parser.add_argument("-f", "--fix",
            action = "store",
            type = int,
            help = "attempts to fix data with too few data points with NACA airfoil equation and input number of desired data points"
            )
    args = parser.parse_args()
    
    new_airfoil = airfoil(args.data_in)

    if args.write:
        if args.scale and args.plot and args.fix:
            new_airfoil.write_new(args.scale, args.fix)
            new_airfoil.plot_data(args.scale, args.fix)
        elif args.scale and args.plot:
            new_airfoil.write_new(args.scale)
            new_airfoil.write_new(args.scale)
        elif args.plot and args.fix:
            new_airfoil.plot_data(args.fix)
        elif args.plot:
            new_airfoil.plot_data()
        else:
            new_airfoil.write_new(fix)
    elif args.plot:
        if args.scale and args.fix:
            new_airfoil.plot_data(args.scale, args.fix)
        elif args.scale:
            new_airfoil.plot_data(args.scale)
        elif args.fix:
            new_airfoil.plot_data(1.0, args.fix)
        else:
            new_airfoil.plot_data()
    else:
        print "Not enough input arguments. Use --help option for required inputs"


