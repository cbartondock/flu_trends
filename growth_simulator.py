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
from standard_plotters import *

def simulate_outbreak(N, mu, ug=True, mp=-1, nes=0):
    #Seeding of Lattice
    seeds = [tuple([0 for i in range(0,d+1)])]
    seeds.extend([tuple([sr()*1000 for j in range(0,d)]) + (0,) for i in range(0, nes)])
    infected_demes = [seed for seed in seeds]
    infection_tracker = Counter() # P: Infected?
    for seed in [seed[:-1] for seed in seeds]:
        infection_tracker[seed] = 1
    #r_of_t = {0 : mean([distance(p, origin) for p in seeds]) } #g: R(g)
    r_of_t = {0 : 1}
    population_dict = {0: len(seeds)}
    generations = [[]]
    generations[0].extend(seeds)
    #Simulation
    i=0
    radii = []
    while (i < N and ug) or (not ug and len(infected_demes) < maxpop):
        i+=1
        print i
        generations.append([])
        for deme in infected_demes:
            Y = r()
            R = (Y*(L**(-mu-1)-C**(-mu-1))+C**(-mu-1))**(-1/(mu+1))
            if d == 2:
                theta = 2*np.pi*r()
                new_infected = (deme[0]+int(R*np.cos(theta)),deme[1]+int(R*np.sin(theta)))
            else:
                new_infected = (deme[0]+ fr()*R,)
            if infection_tracker[new_infected] != 1:
                infection_tracker[new_infected] = 1
                generations[i].append(new_infected + (i,))
        infected_demes.extend(generations[i])

        xav = sum([deme[0] for deme in infected_demes])/len(infected_demes)
        yav = sum([deme[1] for deme in infected_demes])/len(infected_demes)
        r_of_t[i] = gyr_rad(xav, yav, infected_demes)
        population_dict[i] = len(infected_demes)
    print "# demes: {0}".format(len(infected_demes))
    print "# generations: {0}".format(len(generations))
    return [infected_demes, generations, r_of_t, population_dict, (mu,N)]

if __name__ == '__main__':
    #Simulation Parameters
    N = 100

    #Jump Kernel Parameters
    mu = 1.8
    usegenerations = True
    maxpop = -1 if usegenerations else 10**5
    data_dump = simulate_outbreak(N, mu)
    print data_dump[2]
    print data_dump[3]
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
