from universal import *
from kernel_analysis import *
from standard_plotters import *

def seed_lattice(num_extra, extent=20):
    seeds = [tuple([0 for i in range(0,d+2)])]
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

def c_outbreak(mu, mp, seeds = seed_lattice(0), choice_f = trivial_f):
    SIM = CDLL(libraries["outbreak"])
    ARR = CDLL(libraries["array"])
    class Outbreak(Structure):
        pass
    Outbreak._fields_ = [("demes",POINTER(POINTER(c_int))),("used",c_uint),("size",c_uint),("d",c_uint)]
    Outbreak_P = POINTER(Outbreak)
    csim = SIM.sim_cont_outbreak
    csim.restype = Outbreak_P
    outbreak_results = Outbreak_P()
    INT4ARR = c_int*4
    SEEDARR = POINTER(c_int)* len(seeds)
    seeds_ptr = SEEDARR()
    for i in range(0,len(seeds)):
        seeds_ptr[i] = INT4ARR()
        for j in range(0,3):
            seeds_ptr[i][j] = seeds[i][j]
        seeds_ptr[i][3] = choice_f(seeds[i])


    outbreak_results = csim(c_double(mu),
            c_int(mp),
            seeds_ptr,
            c_int(len(seeds)))

    demes = outbreak_results.contents.demes
    infected_demes = [[demes[i][j] for j in range(0,3)] for i in range(0,outbreak_results.contents.used)]
    attr_dict={}
    if(choice_f != trivial_f):
        attr_dict = {(demes[i][0],demes[i][1]):demes[i][3] for i in range(0,outbreak_results.contents.used)}
    ARR.free_outbreak(outbreak_results)
    generations = [[] for i in range(0,infected_demes[-1][2]+1)]
    for deme in infected_demes:
        generations[deme[2]].append(deme)
    genpops = [len(gen) for gen in generations]

    mean_r_of_t, max_r_of_t, gyr_r_of_t, pop_of_t = {},{},{},{}
    for i in range(0,len(generations)):
        xav = mean([deme[0] for j in range(0,i+1) for deme in generations[j]])
        yav = mean([deme[1] for j in range(0,i+1) for deme in generations[j]])
        mean_r_of_t[i] = mean_rad(xav,yav, generations[i])
        max_r_of_t[i] = max_rad(xav,yav, generations[i])
        gyr_r_of_t[i] = gyr_rad(xav,yav, concat(generations,i))
        pop_of_t[i] = sum(genpops[:i+1])
    return {"infected": infected_demes,
            "gens": generations,
            "max_r": max_r_of_t,
            "gyr_r": gyr_r_of_t,
            "mean_r": mean_r_of_t,
            "pop": pop_of_t,
            "attr": attr_dict,
            "params": (mu, mp)}


if __name__ == '__main__':
    args = sys.argv[ 1:]
    mu = 1.5
    mp = 10**5
    seeds = seed_lattice(num_extra=100)
    choice_f = lambda deme: choice([0,1])
    outbreak_data = c_outbreak(mu, mp,seeds=seeds, choice_f = choice_f)

    output_filename = "data_outputs/outbreak_data_mp{0}_mu{1}.pkl".format(tenexp(mp), mu)
    data_output = open(output_filename,'wb')
    pickle.dump(outbreak_data, data_output)
    data_output.close()


#Jump Kernel Analysis
    kernel_filename = analyze_kernel(output_filename)

#Lots of Plotting
    plot_kernel(kernel_filename)
    plot_spread(output_filename)
    plot_radii(output_filename)
    plot_populations(output_filename)
    animate_spread(output_filename)
    if choice_f != trivial_f:
        plot_attr_spread(output_filename)
        animate_attr_spread(output_filename)

