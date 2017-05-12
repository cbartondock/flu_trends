import pickle
from random import random as r
from random import choice
from random import randint
from random import shuffle
from random import sample
import numpy as np
from itertools import chain
import matplotlib
import matplotlib.pylab as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
import sys, time, os
from PIL import Image
import csv
from collections import Counter
from ctypes import *
from multiprocessing import Pool
import multiprocessing
from scipy.optimize import curve_fit

#Latex Parameters
rcParams['axes.labelsize'] = 9
rcParams['xtick.labelsize'] = 9
rcParams['ytick.labelsize'] = 9
rcParams['legend.fontsize'] = 9
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Computer Modern Roman']
rcParams['text.usetex'] = True
rcParams['pgf.texsystem'] = 'lualatex'
rcParams['figure.figsize'] = 7.3, 4.2



#Highly Useful Functions and Constants

origin = (0,0)
d = 2
L=1000000000
C=1

#attribute choice_functions
trivial_f = lambda deme: 0
def rand_choice_f(n_attrs):
    return lambda deme: choice(range(1,n_attrs+1))

def fair_choice_f(n_attrs):
    opts = [i for i in range(1, n_attrs+1)]
    shuffle(opts)
    index=0
    nonlocals = {"opts":opts, "index":index}
    def choice_f(deme):
        result = nonlocals["opts"][nonlocals["index"]]
        nonlocals["index"]= (nonlocals["index"]+1)%len(nonlocals["opts"])
        return result
    return choice_f

def bubble_choice_f(r):
    def choice_f(deme):
        if deme[0]**2 + deme[1]**2 < r**2:
            return 1
        else:
            return 2
    return choice_f

def angle(x,y):
    return (np.arctan(y/x) if x>0 else np.pi+np.arctan(y/x))%(2*np.pi) if x!=0 else (np.pi/2 if y>0 else 3*np.pi/2) if y!=0 else 0

def sector_choice_f(sector_proportions):
    if len(sector_proportions) <2:
        print "Use trivial_f"
        return
    sector_proportions=[entry*2*np.pi/float(sum(sector_proportions)) for entry in sector_proportions]
    def choice_f(deme):
        deme_angle = angle(deme[0],deme[1])
        for i in range(1, len(sector_proportions)+1):
            if deme_angle < sum(sector_proportions[:i]):
                return i
    return choice_f

def seed_lattice(num, choice_f=trivial_f):
    flat_coords = sample(range(0,num**2),num)
    seeds = [(fr()*(flat_coords[i]%(num)),fr()*(flat_coords[i]//num)) for i in range(0, num)]
    seeds = [(seed[0],seed[1],0,choice_f((seed[0],seed[1]))) for seed in seeds]
    return seeds

def seed_disk(R, choice_f=trivial_f):
    seeds =[]
    for i in range(-R,R+1):
        for j in range(-R,R+1):
            if i**2 + j**2 < R**2:
                seeds.append((i,j))
    seeds = [(seed[0],seed[1],0,choice_f((seed[0],seed[1]))) for seed in seeds]
    return seeds

def seed_annulus(r1,r2,choice_f = trivial_f):
    seeds=[]
    for i in range(-r2,r2+1):
        h=int(np.floor(np.sqrt(max(0,r1**2-i**2))**1/2))
        for j in chain(range(-r2,-h),range(h,r2)):
            if i**2+j**2< r2**2 and i**2+j**2>=r1**2:
                seeds.append((i,j))
    seeds = [(seed[0],seed[1],0,choice_f((seed[0],seed[1]))) for seed in seeds]
    return seeds

def get_linear_gens(inf_demes,pergen):
    generations = []
    non_seed_index = 0
    while inf_demes[non_seed_index][2]==0:
        non_seed_index+=1
    generations.append(inf_demes[:non_seed_index])
    inf_demes=inf_demes[non_seed_index:]
    for i in range(0,1+len(inf_demes)//pergen):
        generations.append(inf_demes[pergen*i:min(pergen*(i+1),len(inf_demes))])
    return generations[:-1] if generations[-1]==[] else generations

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


#Choose scaling accordingly
def get_asymptotic_scaling(mu):
    delta = mu-d
    if delta < 0:
        return get_sexp_scaling(delta)
    elif delta > 0:
        return get_powerlaw_scaling(delta)
    return get_critical_scaling()

#This gives the asymptotic first order powerlaw scaling from Oskar's PNAS paper SI
def get_powerlaw_scaling(delta):
    A = np.exp(-2*d*np.log(2) * delta**(-2))
    beta = 1./(delta)
    print "A is " + str(A)
    print "beta is " + str(beta)
    return lambda t: 1 if t==0 else A*(t**beta)

def get_sexp_scaling(delta):
    B = 2*d*np.log(2) * delta**(-2)
    eta = np.log((2*d/(2*d+delta))/np.log(2))
    print "B is " + str(B)
    print "eta is " + str(eta)
    return lambda t: 1 if t==0 else np.exp(B * t**eta)

def get_critical_scaling():
    return lambda t: 1 if t==0 else np.exp((np.log(t)**2) / (4*d*np.log(2)))

#Plotting Helpers
my_colors = map(lambda rgb: (rgb[0]/255.,rgb[1]/255.,rgb[2]/255.), [(240,163,255),(0,117,220),(153,63,0),(76,0,92),(25,25,25),(0,92,49),(43,206,72),(255,204,153),(128,128,128),(148,255,181),(143,124,0),(157,204,0),(194,0,136),(0,51,128),(255,164,5),(255,168,187),(66,102,0),(255,0,16),(94,241,242),(0,153,143),(224,255,102),(116,10,255),(153,0,0),(255,255,128),(255,255,0),(255,80,5)])
shuffle(my_colors)
color_index=0
def rc(advance=True):
    global color_index, my_colors
    result = my_colors[color_index]
    if advance:
        color_index = (color_index + 1)%len(my_colors)
    return result

def tenexp(number):
    return int((np.log(number+.001))/np.log(10.))

#C Interface
libraries = {
        "outbreak": "/Users/chrisdock/Desktop/BioPhys/flu_project/c_code/dylibs/outbreak_sim.dylib",
        "array": "/Users/chrisdock/Desktop/BioPhys/flu_project/c_code/dylibs/dynamic_array.dylib"
}
