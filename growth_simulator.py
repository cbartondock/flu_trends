from universal import *
from kernel_analysis import *
from standard_plotters import *

def seed_lattice(num_extra, extent=20):
    seeds = [tuple([0 for i in range(0,d+1)])]
    seeds.extend([tuple([int(fr()*sr()*extent) for j in range(0,d)]) + (0,) for i in range(0, num_extra)])
    return seeds

def mean_jump(source, mu):
    R = (mu+d-1)/(float)(mu+d-2)
    theta = 2*np.pi*r()
    return (source[0]+int(R*np.cos(theta)),source[1]+int(R*np.sin(theta)))

def jump(source, mu):
    Y = r()
    R = (Y*(L**(-mu-1)-C**(-mu-1))+C**(-mu-1))**(-1/(mu+1))
    theta = 2*np.pi*r()
    return (source[0]+int(R*np.cos(theta)),source[1]+int(R*np.sin(theta)))

def polya_outbreak(N, mu, ug=True, mp=-1, seeds = seed_lattice(0)):
    L=300
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
        gyr_r_of_t[i-1] = gyr_rad(xav, yav, generations[i-1])
        mean_r_of_t[i-1] = mean_rad(xav,yav,generations[i-1])
        pop_of_t[i-1] = len(infected_demes)
        if i==N:
            break
        generations.append([])
        for j in range(0,len(infected_demes)):
            deme_selected = infected_demes[randint(0,len(infected_demes)-1)]
            source = (deme_selected[0],deme_selected[1])
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

def simulate_outbreak(N, mu, ug=True, mp=-1, seeds = seed_lattice(0), choice_f = trivial_f):
    infected_demes = [seed for seed in seeds]
    infection_tracker = Counter()
    attr_dict = {}
    for seed in [seed[:-1] for seed in seeds]:
        infection_tracker[seed] = 1
        if choice_f != trivial_f:
            attr_dict[seed] = choice_f(seed)
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
        gyr_r_of_t[i-1] = gyr_rad(xav, yav, generations[i-1])
        mean_r_of_t[i-1] = mean_rad(xav,yav,generations[i-1])
        pop_of_t[i-1] = len(infected_demes)
        if i==N:
            break
        generations.append([])
        for deme in infected_demes:
            target = jump(deme, mu)
            if infection_tracker[target] != 1:
                infection_tracker[target] = 1
                if choice_f != trivial_f:
                    attr_dict[target] = attr_dict[(deme[0],deme[1])]
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
            "attr": attr_dict,
            "params": (mu,N if ug else mp)}

def c_outbreak(N, mu, ug = True, mp = -1, seeds = seed_lattice(0),choice_f = trivial_f):
    SIM = CDLL(libraries["outbreak"])
    ARR = CDLL(libraries["array"])
    class Outbreak(Structure):
        pass
    Outbreak._fields_ = [("demes",POINTER(POINTER(c_int))),("used",c_uint),("size",c_uint),("d",c_uint)]
    Outbreak_P = POINTER(Outbreak)
    csim = SIM.simulate_outbreak
    csim.restype = Outbreak_P
    my_outbreak = Outbreak_P()
    INT4ARR = c_int*4
    SEEDARR = POINTER(c_int)* len(seeds)
    seeds_ptr = SEEDARR()
    for i in range(0,len(seeds)):
        seeds_ptr[i] = INT4ARR()
        for j in range(0,3):
            seeds_ptr[i][j] = seeds[i][j]
        seeds_ptr[i][3] = choice_f(seeds[i])
    c_ug = 1 if ug else 0
    my_outbreak = csim(c_uint(N),
            c_double(mu),
            c_ubyte(c_ug),
            c_int(mp),
            seeds_ptr,
            c_int(len(seeds)),
            c_int(C),
            c_int(L), 4)
    demes = my_outbreak.contents.demes
    infected_demes = [[demes[i][j] for j in range(0,3)] for i in range(0,my_outbreak.contents.used)]
    attr_dict={}
    if(choice_f != trivial_f):
        attr_dict = {(demes[i][0],demes[i][1]):demes[i][3] for i in range(0,my_outbreak.contents.used)}
    ARR.free_outbreak(my_outbreak)
    generations = [[] for i in range(0,infected_demes[-1][2]+1)]
    for deme in infected_demes:
        generations[deme[2]].append(deme)
    genpops = [len(gen) for gen in generations]

    mean_r_of_t, max_r_of_t, gyr_r_of_t, pop_of_t = {},{},{},{}
    for i in range(0,N):
        xav = mean([deme[0] for j in range(0,i+1) for deme in generations[j]])
        yav = mean([deme[1] for j in range(0,i+1) for deme in generations[j]])
        mean_r_of_t[i] = mean_rad(xav,yav, generations[i])
        max_r_of_t[i] = max_rad(xav,yav, generations[i])
        gyr_r_of_t[i] = gyr_rad(xav,yav, concat(generations,i))
        pop_of_t[i] = sum(genpops[:i+1])
    #print "# demes: {0}".format(len(infected_demes))
    #print "# generations: {0}".format(len(generations))
    return {"infected": infected_demes,
            "gens": generations,
            "max_r": max_r_of_t,
            "gyr_r": gyr_r_of_t,
            "mean_r": mean_r_of_t,
            "pop": pop_of_t,
            "attr": attr_dict,
            "params": (mu, N if ug else mp)}


if __name__ == '__main__':
    args = sys.argv[1:]

    N = 50
    mu = 1.8
    usegenerations = True
    maxpop = -1 if usegenerations else 10**5
    choice_f = lambda p: choice([0,1])

    if len(args)==0 or args[0]=="normal":
        data_dump = simulate_outbreak(N,mu,seeds=seed_lattice(100),choice_f=choice_f)
    elif args[0] == "polya":
        data_dump = polya_outbreak(N, mu)
    elif args[0] == "c":
        data_dump = c_outbreak(N,mu,seeds=seed_lattice(100),choice_f=choice_f)

    output_filename = "data_outputs/{0}_data_{1}{2}_mu{3}".format("normal" if len(args)==0 else args[0],"N" if usegenerations else "P", N if usegenerations else maxpop, mu)
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

