from universal import *
from kernel_analysis import *
from standard_plotters import *

def c_outbreak(mu, mp, seeds = seed_lattice(1)):
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
        for j in range(0,4):
            seeds_ptr[i][j] = seeds[i][j]

    outbreak_results = csim(c_double(mu),
            c_int(mp),
            seeds_ptr,
            c_int(len(seeds)))

    demes = outbreak_results.contents.demes
    n_inf_demes = outbreak_results.contents.used
    infected_demes = [[demes[i][j] for j in range(0,3)] for i in range(0, n_inf_demes)]
    attr_dict = {} if seeds[0][3]==0 else {(demes[i][0],demes[i][1]):demes[i][3] for i in range(0, n_inf_demes)}

    generations = [[] for i in range(0,infected_demes[-1][2]+1)]
    for deme in infected_demes:
        generations[deme[2]].append(deme)
    generations = [gen for gen in generations if gen!=[]]
    genpops = [len(gen) for gen in generations]

    mean_r_of_t, max_r_of_t, pop_of_t = {},{},{}
    for i in range(0,len(generations)):
        xav = mean([deme[0] for j in range(0,i+1) for deme in generations[j]])
        yav = mean([deme[1] for j in range(0,i+1) for deme in generations[j]])
        mean_r_of_t[i] = mean_rad(xav,yav, generations[i])
        max_r_of_t[i] = max_rad(xav,yav, generations[i])
        if i>0 and max_r_of_t[i-1]>max_r_of_t[i]:
            max_r_of_t[i] = max_r_of_t[i-1]
        pop_of_t[i] = sum(genpops[:i+1])

    ARR.free_outbreak(outbreak_results)
    return {"infected": infected_demes,
            "gens": generations,
            "max_r": max_r_of_t,
            "mean_r": mean_r_of_t,
            "pop": pop_of_t,
            "attr": attr_dict,
            "params": {"mu":mu, "mp":mp}}


if __name__ == '__main__':
    args = sys.argv[1:]
    mp = int(.5*10**4)
    mu=1.8
    choice_f=rand_choice_f(3)
    seeds = seed_disk(30, choice_f)
    outbreak_data = c_outbreak(mu, mp, seeds=seeds)
    output_filename = "data_outputs/outbreak_data_mp{0}_mu{1}.pkl".format(tenexp(mp), mu)
    data_output = open(output_filename,'wb')
    pickle.dump(outbreak_data, data_output)
    data_output.close()
    print "#gens: " + str(len(outbreak_data["gens"]))


#Jump Kernel Analysis
    kernel_filename = analyze_kernel(output_filename)

#Lots of Plotting
    t=str(round(time.time()))
    #plot_kernel(kernel_filename,t)
    plot_spread(output_filename,t)
    plot_radii(output_filename,t)
    plot_populations(output_filename,t)

    if seeds[0][3]!=0:
        plot_frequencies(output_filename,t)
        plot_similarity(choice_f,output_filename,t)
        plot_attr_spread(output_filename,t)
        animate_attr_spread(output_filename,t)

