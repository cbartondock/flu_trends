import pickle
import random
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pylab as plt
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
import matplotlib.animation as animation
import sys
from collections import Counter

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
distance = lambda p1, p2: ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**.5
mean = lambda l: 0 if len(l)==0 else sum(l)/float(len(l))
even_round = lambda x: int(x) if (x%1==.5 and not(int(x)%2)) else int(round(x))
origin = (0,0)
d=2

def time_average(data):
    """Works on data of the form [(t0, a), (t1, b), (t2, c),...]"""
    d = {t: [] for t in range(0, max(data, key = lambda tup: tup[0])[0]+1)} #Python is Wizardry
    for tup in data:
        d[tup[0]].append(tup[1])
    return [(k, mean(v)) for k, v in d.items()]
