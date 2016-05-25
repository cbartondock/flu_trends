from growth_simulator import *
from universal import *

def analyze_predictability(init_N, N, mu, n_sim):
    seeds = [(deme[0],deme[1],0) for deme in simulate_outbreak(init_N, mu)["infected"]]
    infected_states = {g: [] for g in range(0,N)}

    for i in range(0, n_sim):
        print i
        data = simulate_outbreak(N, mu, seeds = seeds)
        for g in range(0,N):
            infected_states[g].append(concat(data["gens"],g))
    max_extents, max_mean, max_fluct = {g: None for g in range(0,N)},{g: None for g in range(0,N)},{g: None for g in range(0,N)}
    gyr_extents, gyr_mean, gyr_fluct = {g: None for g in range(0,N)},{g: None for g in range(0,N)},{g: None for g in range(0,N)}
    pops, pop_mean, pop_fluct = {g: None for g in range(0,N)},{g: None for g in range(0,N)},{g: None for g in range(0,N)}

    for g in range(0, N):
        max_extents[g] = [max_rad(0,0,state) for state in infected_states[g]]
        gyr_extents[g] = [gyr_rad(0,0,state) for state in infected_states[g]]
        pops[g] = [len(state) for state in infected_states[g]]
        max_mean[g] = mean(max_extents[g])
        gyr_mean[g] = mean(gyr_extents[g])
        pop_mean[g] = mean(pops[g])
        max_fluct[g] = mean([(max_extent - max_mean[g])**2 for max_extent in max_extents[g]])**.5/max_mean[g]
        gyr_fluct[g] = mean([(gyr_extent -gyr_mean[g])**2 for gyr_extent in gyr_extents[g]])**.5/gyr_mean[g]
        pop_fluct[g] = mean([(pop - pop_mean[g])**2 for pop in pops[g]])**.5/pop_mean[g]
    return max_fluct, gyr_fluct, pop_fluct

if __name__ == '__main__':
    init_N = 10
    N = 50
    mu = 1.8
    n_sim = 500
    max_f, gyr_f, pop_f = analyze_predictability(init_N,N, mu, n_sim)

    plt.suptitle(r'Averaged Fluctuations over {0} generations with {2} seed generations, $\mu={1}$'.format(N, mu, init_N),  fontweight='bold')
    f, (fluct_ax1,fluct_ax2)  = plt.subplots(1,2)
    gyrplot = fluct_ax1.scatter(list(range(0,N)),[gyr_f[g] for g in range(0,N)], color=rc())
    maxplot = fluct_ax1.scatter(list(range(0,N)),[max_f[g] for g in range(0,N)], color=rc())
    popplot = fluct_ax2.scatter(list(range(0,N)),[pop_f[g] for g in range(0,N)], color=rc())
    fluct_ax1.set_xlabel(r'Generation')
    fluct_ax1.set_ylabel(r'Fluctuation')
    fluct_ax1.legend(handles=[gyrplot,maxplot],labels=[r'Gyration Radius Fluctuation', r'Maximum Radius Fluctuation'], loc='upper left')
    fluct_ax2.set_xlabel(r'Generation')
    fluct_ax2.set_ylabel(r'Fluctuation ')
    fluct_ax2.legend(handles=[popplot],labels=[r'Population Fluctuation'])
    plt.savefig("outputs/average_fluctuation_plot_N{0}_mu{1}_Ns{2}.png".format(N,mu,init_N),dpi=400)

