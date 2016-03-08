""" This program uses a d-lattice  and a jump kernel to simulate the spread of an epidemic
that involves long range jumps
d - lattice dimension
N - # of generations (if generation cap in place)
mu - mu value in kernel
L - Scale Parameter for kernel
C - Scale Parameter for kernel
ug - use generation cap?
mp - max population (if population cap in place)
nes - # of extra randomly placed seeds (0 by default)
"""

from universal import *
from kernel_analysis import *
from plotters import *

def simulate_outbreak(d, N, mu, ug, mp, nes=0, L=1000000000, C=1):
    #Seeding of Lattice
    seeds = [tuple([0 for i in range(0,d+1)])]
    seeds.extend([tuple([sr()*1000 for j in range(0,d)]) + (0,) for i in range(0, nes)])
    infected_demes = [seed for seed in seeds]
    infection_tracker = Counter() # P: Infected?
    for seed in [seed[:-1] for seed in seeds]:
        infection_tracker[seed] = 1
    r_of_t = {0 : mean([distance(p, origin) for p in seeds]) } #g: R(g)
    population_dict = {0: len(seeds)}
    generations = [[]]
    generations[0].extend(seeds)
    print infected_demes
    #Simulation
    i=0
    radii = []
    while (i < N and ug) or (not ug and len(infected_demes) < maxpop):
        i+=1
        print i
        generations.append([])
        for deme in infected_demes:
            Y = r()
            R = (Y*(L**(-mu)-C**(-mu))+C**(-mu))**(-1/mu)
            if d == 2:
                theta = 2*np.pi*r()
                new_infected = (deme[0]+int(R*np.cos(theta)),deme[1]+int(R*np.sin(theta)))
            else:
                new_infected = (deme[0]+ fr()*R,)
            if infection_tracker[new_infected] != 1:
                infection_tracker[new_infected] = 1
                generations[i].append(new_infected + (i,))
        infected_demes.extend(generations[i])
        #r_of_t[i] = max(map(lambda p: p[0]**2+p[1]**2, infected_demes))**.5
        """if d==2:
            r_of_t[i] = mean([distance(p, origin) for p in infected_demes])
        else:
            r_of_t[i] = mean([distance_1d(p, origin) for p in infected_demes])"""
        r_of_t[i] = (len(infected_demes)/np.pi)**.5
        #r_of_t[i] = mean([distance(p,origin) for p in generations[i]])
        #r_of_t[i] = (len(infected_demes)/np.pi)**.5
        population_dict[i] = len(infected_demes)
    print "# demes: {0}".format(len(infected_demes))
    print "# generations: {0}".format(len(generations))
    return [infected_demes, generations, r_of_t, population_dict, (L,mu,N,d)]

if __name__ == '__main__':
    #Simulation Parameters
    N = 30

    #Jump Kernel Parameters
    mu = 2.0
    usegenerations = True
    maxpop = -1 if usegenerations else 10**5
    data_dump = simulate_outbreak(d, N, mu, usegenerations, maxpop)
    print "Saving Simulation Data"
    if usegenerations:
        output_filename = "data_outputs/simulation_data_N{0}_mu{1}.pkl".format(N,mu)
    else:
        output_filename = "data_outputs/simulation_data_P{0}_mu{1}.pkl".format(maxpop,mu)
    data_output = open(output_filename,'wb')
    pickle.dump(data_dump, data_output)
    data_output.close()


#Jump Kernel Analysis (super simple first, will get clever)
    kernel_filename = analyze_kernel(output_filename)

#Lots of Plotting
    plot_kernel(kernel_filename)
    plot_spread(output_filename)
    plot_radii(output_filename)
    plot_populations(output_filename)
