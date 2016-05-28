from universal import *
from kernel_analysis import *
from standard_plotters import *

def seed_lattice(num_extra, extent=10):
    seeds = [tuple([0 for i in range(0,d+1)])]
    seeds.extend([tuple([fr()*sr()*extent for j in range(0,d)]) + (0,) for i in range(0, num_extra)])
    return seeds

def jump(source, mu):
    Y = r()
    R = (Y*(L**(-mu-1)-C**(-mu-1))+C**(-mu-1))**(-1/(mu+1))
    theta = 2*np.pi*r()
    return (source[0]+int(R*np.cos(theta)),source[1]+int(R*np.sin(theta)))

def polya_outbreak(N, mu, ug=True, mp=-1, seeds = seed_lattice(0)):
    infected_demes = [seed for seed in seeds]
    infection_tracker = Counter()
    for seed in [seed[:-1] for seed in seeds]:
        infection_tracker[seed] = 1
    generations = [[]]
    generations[0].extend(seeds)
    gyr_r_of_t = {}
    max_r_of_t = {}
    mean_r_of_t = {}
    pop_of_t = {}

    i=1
    while (ug and i <= N) or (not ug and len(infected_demes) < maxpop):
        xav = mean([deme[0] for deme in infected_demes])
        yav = mean([deme[1] for deme in infected_demes])
        max_r_of_t[i-1] = max_rad(xav, yav, generations[i-1])
        gyr_r_of_t[i-1] = gyr_rad(xav, yav, infected_demes)
        mean_r_of_t[i-1] = mean_rad(xav,yav,generations[i-1])
        pop_of_t[i-1] = len(infected_demes)
        if i==N:
            break
        generations.append([])
        for j in range(0,L**d):
            source = (fr()*randint(0,L//2),fr()*randint(0,L//2))
            if infection_tracker[source]:
                target = jump(source, mu)
                if infection_tracker[target] != 1:
                    infection_tracker[target] = 1
                    generations[i].append(target + (i,))
        infected_demes.extend(generations[i])
        i+=1

    print "# demes: {0}".format(len(infected_demes))
    print "# generations: {0}".format(len(generations))
    return {"infected": infected_demes,
            "gens": generations,
            "max_r": max_r_of_t,
            "gyr_r": gyr_r_of_t,
            "mean_r": mean_r_of_t,
            "pop": pop_of_t,
            "params": (mu,N if ug else mp)}

def simulate_outbreak(N, mu, ug=True, mp=-1, seeds = seed_lattice(0)):
    infected_demes = [seed for seed in seeds]
    infection_tracker = Counter()
    for seed in [seed[:-1] for seed in seeds]:
        infection_tracker[seed] = 1
    generations = [[]]
    generations[0].extend(seeds)
    gyr_r_of_t = {}
    max_r_of_t = {}
    mean_r_of_t = {}
    pop_of_t = {}

    i=1
    while (ug and i <= N) or (not ug and len(infected_demes) < maxpop):
        xav = mean([deme[0] for deme in infected_demes])
        yav = mean([deme[1] for deme in infected_demes])
        max_r_of_t[i-1] = max_rad(xav, yav, generations[i-1])
        gyr_r_of_t[i-1] = gyr_rad(xav, yav, infected_demes)
        mean_r_of_t[i-1] = mean_rad(xav,yav,generations[i-1])
        pop_of_t[i-1] = len(infected_demes)
        if i==N:
            break
        generations.append([])
        for deme in infected_demes:
            target = jump(deme, mu)
            if infection_tracker[target] != 1:
                infection_tracker[target] = 1
                generations[i].append(target + (i,))
        infected_demes.extend(generations[i])
        i+=1

    print "# demes: {0}".format(len(infected_demes))
    print "# generations: {0}".format(len(generations))
    return {"infected": infected_demes,
            "gens": generations,
            "max_r": max_r_of_t,
            "gyr_r": gyr_r_of_t,
            "mean_r": mean_r_of_t,
            "pop": pop_of_t,
            "params": (mu,N if ug else mp)}

def c_outbreak(N, mu, ug = True, mp = -1, seeds = seed_lattice(0)):
    SIM = CDLL(libraries["outbreak"])
    seeds = np.array(seeds).astype(int)
    class Outbreak(Structure):
        pass

    Outbreak._fields_ = [("demes",POINTER(POINTER(c_int))),("used",c_uint),("size",c_uint)]
    Outbreak_P = POINTER(Outbreak)
    csim = SIM.simulate_outbreak
    csim.restype = Outbreak_P
    my_outbreak = Outbreak_P()
    my_outbreak = csim(c_uint(N),
            c_double(mu),
            c_ubyte(ug),
            c_int32(mp),
            (POINTER(c_int32)*len(seeds))(*[deme.ctypes.data_as(POINTER(c_int32)) for deme in seeds]),
            c_int32(len(seeds)),
            c_int32(C),
            c_int32(L))
    print "used is " +str(my_outbreak.contents.used)
    test = my_outbreak.contents.demes
    print "deme_test " +str([[test[i][j] for j in range(0,3)] for i in range(0,N)])
    """infected_demes = []
    for i in range(0, my_outbreak.contents.used):
        infected_demes.append([my_outbreak.contents.demes[i][j] for j in range(0,3)])
    print infected_demes"""





if __name__ == '__main__':
    args = sys.argv[1:]

    N = 5
    mu = 1.8
    usegenerations = True
    maxpop = -1 if usegenerations else 10**5

    if len(args)==0 or args[0]=="normal":
        data_dump = simulate_outbreak(N, mu)
    elif args[0] == "polya":
        data_dump = polya_outbreak(N, mu)
    elif args[0] == "c":
        data_dump =c_outbreak(N,mu)

"""
    output_filename = "data_outputs/{0}_data_{1}{2}_mu{3}".format("polya" if polya else "simulation","N" if usegenerations else "P", N if usegenerations else maxpop, mu)
    data_output = open(output_filename,'wb')
    pickle.dump(data_dump, data_output)
    data_output.close()

#Jump Kernel Analysis
    kernel_filename = analyze_kernel(output_filename)

#Lots of Plotting
    plot_kernel(kernel_filename)
    plot_spread(output_filename)
    plot_radii(output_filename)
    plot_populations(output_filename)
"""
