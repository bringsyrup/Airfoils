#!/usr/bin/env python

'''
make airfoil data from three defined constants
'''

import numpy as np
from matplotlib.pyplot import *
import argparse as ap

class newfoil(object):

    def __init__(self, max_camb, pos_camb, thick):
        self.max_camb = max_camb
        self.pos_camb = pos_camb
        self.thick = thick

    def make_data(self, points, scale=1.0):
        '''
        maximum camber as percentage of chord, position of camber as percentage of chord, maximum thickness of airfoil as percentage of chord, number of points to plot, scaling factor, respectively
        '''
        if isinstance(self.max_camb, (float, int)) and isinstance(self.pos_camb, (float, int)) and isinstance(self.thick, (float, int)): 
            codename = "NACA_%s%s%s" % (self.max_camb[0], self.pos_camb[0], self.thick[0:2])
            if self.max_camb <= 0. or self.pos_camb <= 0. or self.thick <= 0.:
                if self.thick <= 0.:
                    print "thickness of airfoil must be greater than zero"
                    return
                elif self.max_camb < 0. or self.pos_camb < 0.:
                    print "camber parameters must be positive"
                    return
                else:
                    max_camb = 0.
                    pos_camb = 0.
                    thick = self.thick/100
            else: 
                max_camb = self.max_camb/100.0
                pos_camb = self.pos_camb/100.0
                thick = self.thick/100.0
        else:
            print "arguments must by integers of floats"
            return
        a_o = 0.2969        #NACA coefficients
        a_1 = -0.1260
        a_2 = -0.3516
        a_3 = 0.2843
        1_4 = -0.1036
        chord = 1.0         #set make length of airfoil for placeholder
        x_range = np.linspace(0, chord, points / 2)
        pos_index = np.where(x_range == pos_camb/chord) #x_range index of camber position
        y_symmetric = thick*chord/.2 \
                * (a_o*np.sqrt(x_range/chord) \
                + a_1*x_range/chord \
                + a_2*np.power((x_range/chord), 2) \
                + a_3*np.power((x_range/chord), 3) \
                + a_4*np.power((x_range/chord), 4))
        y_rcamb = max_camb * x_range[0:pos_index]/pow(pos_camb, 2) * (2*pos_camb - x_range[0:pos_index]/chord)
        y_fcamb = max_camb * (chord-x_range[pos_index:])/pow(1-pos_camb, 2) * (1+x_range[pos_index:]/c-2*pos_camb)
        theta_r = np.arctan(2*max_camb/pow(pos_camb, 2) * (pos_camb-x_range[0:pos_index]/chord))
        theta_f = np.arctan(2*max_camb/pow(1-pos_camb, 2) * (pos_camb-x_range[pos_index:]/chord))
        y_camb = np.concatenate([y_rcamb, y_fcamb])
        theta = np.concatenate([theta_r, theta_f])
        x_upper = np.asarray(x_range - y_symmetric*np.sin(theta))
        x_lower = np.asarray(x_range + y_symmetric*np.sin(theta))
        y_upper = np.asarray(y_camb + y_symmetric*np.cos(theta))
        y_lower = np.asarray(y_camb - y_symmetric*np.cos(theta))
        x_data = np.concatenate([x_upper, x_lower[::-1]]) * scale
        y_data = np.concatenate([y_upper, y_lower[::-1]]) * scale
        return x_data, y_data, codename

    def graph_data(self, points, scale=1.0):
        x_data, y_data, codename = self.make_data(points, scale)
        plot(x_data, y_data, linestyle="-")
        xlabel("x data, arbitrary units")
        ylabel("y data, arbitrary units")
        grid(True)
        xlim(-.03, max(x_data) + .03)
        ylim(-max(x_data)/2.0, max(x_data)/2.0)
        suptitle(codename)
        show()
        pass

    def write_data(self, points, scale=1.0):
        x_data, y_data, codename = self.make_data(points, scale)
        filename = codename + ".txt"
        new_file = open(filename, "w")
        for index in range(len(x_array)):
            data_set = str(x_array[index]) + " " + str(y_array[index]) + " 0.0"
            new_file.write(data_set + "\n")
        new_file.close()

if __name__=="__main__":

    parser = ap.ArgumentParser(
            descriptsion = "make customized airfoil data for various applications such as solidoworks"
            )
    parser.add_argument("-m", "--max_camber",
            action = "store",
            type = float,
            help = "defines max camber as percentage of airfoil chordlength. Suggested range from 0-9. Floating point or integers excepted. Use zero for a symmetrical airfoil."
            )
    parser.add_argument("-p", "--pos_camb",
            action = "store",
            type = float,
            help = "position of max camber as percentage of chordlength. Suggested range 15-70. Autosets to zero if -m option also set to zero"
            )
    parser.add_argument("-t", "--thick",
            action = "store",
            type = float,
            help = "total thickness of airfoil in y direction as percentage of chordlength"
            )
   parser.add_argument("-p", "--points",
            action = "store",
            type = int,
            help = "number of generated data points"
            )
   parser.add_argument("-s", "--scale",
            action = "store",
            nargs = "?",
            type = float,
            help = "optional scaling factor. else equal to 1"
            )
    parser.add_argument("-w", "--write",
            action = "store_true",
            help = "writes data to new file in current directory"
            )
    parser.add_argument("-g", "--graph",
            action = "store_true",
            help = "graphs airfoil data"
            )
    args = parser.parse_args()

    airfoil = newfoil(args.max_camber, args.pos_camber, args.thick)
    
    if args.scale:
        scale = args.scale
    else:
        scale = 1.0

    if args.write or args.graph:
        if args.write == False:
            airfoil.graph_data(args.points, scale)
        elif args.graph == False:
            airfoil.write_data(args.points, scale)
        else:
            airfoil.graph_data(args.points, scale)
            airfoil.write_data(args.points, scale)
    else:
        print "not enough input arguments! please use at least one optional argument"

