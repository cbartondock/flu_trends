from growth_simulator import simulate_outbreak
from universal import *

#analagous to spacetime interval in Special Relativity
disease_interval = lambda source, child, scaling: ((child[0]-source[0])**2 - scaling(child[1]-source[1])**2)/scaling(child[1]-source[1])**2

i=0

def adapt_guess(guess, children):
    disease_interval_dist = [child for tree in children.values() for child in tree]
    print disease_interval_dist
    plt.hist(disease_interval_dist, 100)
    global i
    plt.savefig("scaling_figs/{0}.png".format(i))
    plt.clf()
    i+=1
    return guess

def scaling(future, initial_guess):
    if len(future) == 1:
        return initial_guess
    n_guess = scaling(future[1:], initial_guess)
    pot_children = [child for gen in future[1:] for child in gen]
    children = {deme: filter(lambda x:x<0, [disease_interval(deme,child,n_guess) for child in pot_children]) for deme in future[0]}
    return adapt_guess(n_guess, children)

if __name__ == '__main__':
    data_from_outbreak = simulate_outbreak(1,5, 2.0, True, -1, 3)[1]
    #print [(int(p[0]),p[1]) for g in data_from_outbreak for p in g]
    l = scaling(data_from_outbreak, lambda t: 3*t)
    #print l(5)

