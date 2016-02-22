""" This program uses a d-lattice  and a jump kernel to simulate the spread of an epidemic
that involves long range jumps"""

from universal import *
from kernel_analysis import *
from plotters import *

def simulate_outbreak(d, N, mu, L, C):
    #seeding of Lattice
    seed = tuple([0 for i in range(0,d)])
    infected_demes = [seed]
    infection_tracker = Counter() # P: Infected?
    generation_dict={seed: 0} #P: Color num
    r_of_t={0:0.} #N: R
#rav_of_t={0:0.}
    population_dict = {0: 1}
    generations = [[] for i in range(0,N+1)]
    generations[0].append((seed[0],seed[1],0.))
#Simulation
    print "Running Simulation"
    i=0
    radii = []
    while i < N:
        print i
        i+=1
        for deme in infected_demes:
            Y = random.random()
            R = (Y*(L**(-mu)-C**(-mu))+C**(-mu))**(-1/mu)
            theta = 2*np.pi*random.random()
            new_infected = (deme[0]+int(R*np.cos(theta)),deme[1]+int(R*np.sin(theta)))
            if not infection_tracker[new_infected]:
                infection_tracker[new_infected]=1
                infected_demes.append(new_infected)
                generations[i].append((new_infected[0], new_infected[1],i))
                generation_dict[new_infected] = i
        #r_of_t[i] = max(map(lambda p: p[0]**2+p[1]**2, infected_demes))**.5
        r_of_t[i] = mean([distance(p, origin) for p in infected_demes])

        population_dict[i] = len(infected_demes)
    infected_demes=map(lambda deme: (deme[0], deme[1], generation_dict[deme]), infected_demes)
    return [infected_demes, generations, r_of_t, population_dict, (L,mu,N,d)]

if __name__ == '__main__':
    #Simulation Parameters
    N = 20

    #Jump Kernel Parameters
    mu = 2.5
    C=1
    L=1000000000

    data_dump = simulate_outbreak(d, N, mu, L, C)
    print "Saving Simulation Data"
    output_filename = "data_outputs/simulation_data_N{0}_mu{1}_L{2}.pkl".format(N,mu,L)
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
