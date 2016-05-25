import pickle
from random import random as r
from random import choice
from random import randint
import numpy as np
from itertools import chain
import matplotlib
import matplotlib.pylab as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import sys, time
from collections import Counter
from ctypes import *

#Latex Parameters
rcParams['axes.labelsize'] = 9
rcParams['xtick.labelsize'] = 9
rcParams['ytick.labelsize'] = 9
rcParams['legend.fontsize'] = 9
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Computer Modern Roman']
rcParams['text.usetex'] = True
rcParams['figure.figsize'] = 7.3, 4.2


#Highly Useful Functions and Constants

origin = (0,0)
d = 2
L=150
C=1

sr = lambda : 2*(r()-.5)
fr = lambda : choice([-1,1])
distance = lambda p1, p2: ( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )**.5
distance_1d = lambda p1, p2: abs(p1[0] - p2[0])
mean = lambda l: 0 if len(l)==0 else sum(l) / float(len(l))
even_round = lambda x: int(x) if (x%1==.5 and not(int(x)%2)) else int(round(x))
concat = lambda l, i: list(chain.from_iterable(l[:i+1]))

mean_rad = lambda x0, y0, l: mean([((p[0]-x0)**2+(p[1]-y0)**2)**.5 for p in l])
gyr_rad = lambda x0, y0, l: mean([(p[0]-x0)**2+(p[1]-y0)**2 for p in l])**.5
area_rad = lambda x0, y0, l: (len(infected_demes)/np.pi)**.5
max_rad = lambda x0, y0, l: 0 if len(l)==0 else max([((p[0]-x0)**2+(p[1]-y0)**2)**.5 for p in l])


def time_average(data):
    """Works on data of the form [(t0, a), (t1, b), (t2, c),...]"""
    d = {t: [] for t in range(0, max(data, key = lambda tup: tup[0])[0]+1)} #Python is Wizardry
    for tup in data:
        d[tup[0]].append(tup[1])
    return [(k, mean(v)) for k, v in d.items()]


#This gives the crossover scaling from Oskar's PNAS paper SI
def get_crossover_scaling(mu):
    delta = mu - d
    h = 2*d/delta
    z = lambda t: np.log2(t)
    return lambda t: 1 if t==0 else 2**((h/delta)*(z(t)/h + (1+1/h)**(-z(t))-1))

#This gives the asymptotic zeroth order powerlaw scaling from Oskar's PNAS paper SI
def get_powerlaw_scaling(mu):
    delta = mu - d
    A = 2**(-2*d/(delta**2))
    beta = -1./(delta)
    return lambda t: 1 if t==0 else A*(t**beta)


def get_sexp_scaling(mu):
    delta = mu - d
    B = 2*d/(delta**2)
    eta = log((2*d/(d+mu)))/log(2)
    return lambda t: 1 if t==0 else 2**(B*(t**eta))

def get_sexp_scaling_corrected(mu):
    delta = mu
    B = 2*d/(delta**2)
    eta = log((2*d/(d+mu)))/log(2)
    #unfinished (pending math)


#Plotting Helpers
my_colors = map(lambda rgb: (rgb[0]/255.,rgb[1]/255.,rgb[2]/255.), [(240,163,255),(0,117,220),(153,63,0),(76,0,92),(25,25,25),(0,92,49),(43,206,72),(255,204,153),(128,128,128),(148,255,181),(143,124,0),(157,204,0),(194,0,136),(0,51,128),(255,164,5),(255,168,187),(66,102,0),(255,0,16),(94,241,242),(0,153,143),(224,255,102),(116,10,255),(153,0,0),(255,255,128),(255,255,0),(255,80,5)])
rc = lambda : my_colors[randint(0,len(my_colors)-1)]

#C Interface
libraries = {
        "outbreak":"c_code/dylibs/outbreak_sim.dylib"
        }
