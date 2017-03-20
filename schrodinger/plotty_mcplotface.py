from efficient_wk5 import hydrogen_wave_func

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

### PRINTERS ###
CYAN  = "\033[1;36m"
GREEN = "\033[1;32m"
RED   = "\033[1;31m"
RESET = "\033[1;0m"

def print_color_generator(C):
    def print_color(*strs):
        print C + ' '.join(strs) + RESET

    return print_color

cyan, green, red = map(print_color_generator, [CYAN, GREEN, RED])

### STARTING FURREAL ###

def get_plot(n, l, m):
    cyan('CALCULATING VALUES FOR n: {}, l: {}, m: {}....'.format(n, l, m))

    x, y, z, mag = hydrogen_wave_func(n, l, m, 10, 20, 20, 20)

    green('EUREKA!')
    cyan('Plotting....')

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for a in range(0,len(mag)):
        for b in range(0,len(mag)):
            for c in range(0,len(mag)):
                ax.scatter(x[a][b][c],y[a][b][c],z[a][b][c], marker='o',
                    alpha=(mag[a][b][c]/np.amax(mag)))

    return plt

def plot_n_save(n):
    for l in range(n):
        for m in range(l+1):
            plt = get_plot(n, l, m)
            filename = 'n{}_m{}_l{}.png'.format(n, m, l)
            plt.savefig(filename)

            green('SUCCESS! File saved as {}'.format(filename))
            print '\n\n\n'

plot_n_save(2)
