from growth_simulator import simulate_outbreak
from universal import *

init_mu = 1.5
actual_mu = 1.5

def get_scaling(mu, d):
    delta = mu - d
    h = 2*d/delta
    return lambda t: 2**((h/delta)*(np.log2(t)/h + (1+1/h)**(-np.log2(t))-1))

#analagous to spacetime interval in Special Relativity
disease_interval = lambda source, child, mu: ((child[0]-source[0])**2 - get_scaling(mu, 1)(child[1]-source[1])**2)/get_scaling(mu,1)(child[1]-source[1])**2

i=0
def adapt_guess(guess, children):
    disease_interval_dist = [child for tree in children.values() for child in tree]
    print disease_interval_dist
    plt.hist(disease_interval_dist, 100)
    global init_mu, actual_mu, i
    plt.savefig("scaling_figs/initmu_{0}_actualmu_{1}_{2}.png".format(init_mu,actual_mu, i))
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
    data_from_outbreak = simulate_outbreak(1,20, actual_mu, True, -1, 3)[1]
    #print [(int(p[0]),p[1]) for g in data_from_outbreak for p in g]
    l = scaling(data_from_outbreak, init_mu)

