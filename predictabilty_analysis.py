from growth_simulator import *
from universal import *


def distributions_of_time(init_N, N, mu, n_sim):
    seeds = [[deme[0],deme[1],0] for deme in c_outbreak(init_N, mu)["infected"]]
    infected_states = {g: [] for g in range(0,N)}

    for i in range(0, n_sim):
        print i
        data = c_outbreak(N, mu, seeds = seeds)
        for g in range(0,N):
            infected_states[g].append(concat(data["gens"],g))
    max_extents = {g: None for g in range(0,N)}
    gyr_extents = {g: None for g in range(0,N)}
    pops = {g: None for g in range(0,N)}
    for g in range(0,N):
        max_extents[g] = [max_rad(0,0,state) for state in infected_states[g]]
        gyr_extents[g] = [gyr_rad(0,0,state) for state in infected_states[g]]
        pops[g] = [len(state) for state in infected_states[g]]
    return max_extents, gyr_extents, pops


def fluctuation_of_time(init_N, N, mu, n_sim):
    max_mean, max_fluct = {g: None for g in range(0,N)},{g: None for g in range(0,N)}
    gyr_mean, gyr_fluct = {g: None for g in range(0,N)},{g: None for g in range(0,N)}
    pop_mean, pop_fluct = {g: None for g in range(0,N)},{g: None for g in range(0,N)}
    max_extents, gyr_extents, pops = distributions_of_time(init_N, N, mu, n_sim)
    for g in range(0, N):
        max_mean[g] = mean(max_extents[g])
        gyr_mean[g] = mean(gyr_extents[g])
        pop_mean[g] = mean(pops[g])
        max_fluct[g] = mean([(max_extent - max_mean[g])**2 for max_extent in max_extents[g]])**.5/max_mean[g]
        gyr_fluct[g] = mean([(gyr_extent -gyr_mean[g])**2 for gyr_extent in gyr_extents[g]])**.5/gyr_mean[g]
        pop_fluct[g] = mean([(pop - pop_mean[g])**2 for pop in pops[g]])**.5/pop_mean[g]
    return max_fluct, gyr_fluct, pop_fluct



if __name__ == '__main__':
    init_N = 10
    N = 5
    mu = 1.8
    n_sim = 100

    args = sys.argv[1:]
    if len(args)==0 or args[0] == "fluctuations":
        max_f, gyr_f, pop_f = fluctuation_of_time(init_N,N, mu, n_sim)
        plt.suptitle(r'Averaged Fluctuations over {0} generations with {2} seed generations, $\mu={1}$'.format(N, mu, init_N),  fontweight='bold')
        f, (fluct_ax1,fluct_ax2)  = plt.subplots(1,2)
        gyrplot = fluct_ax1.scatter(list(range(0,N)),[gyr_f[g] for g in range(0,N)], color=rc())
        maxplot = fluct_ax1.scatter(list(range(0,N)),[max_f[g] for g in range(0,N)], color=rc())
        popplot = fluct_ax2.scatter(list(range(0,N)),[pop_f[g] for g in range(0,N)], color=rc())
        fluct_ax1.set_xlabel(r'Generation')
        fluct_ax1.set_ylabel(r'Fluctuation')
        fluct_ax1.legend(handles=[gyrplot,maxplot],labels=[r'Gyration Radius Fluctuation', r'Maximum Radius Fluctuation'], loc='upper left')
        fluct_ax2.set_xlabel(r'Generation')
        fluct_ax2.legend(handles=[popplot],labels=[r'Population Fluctuation'])
        plt.savefig("outputs/average_fluctuation_plot_N{0}_mu{1}_Ns{2}.png".format(N,mu,init_N),dpi=400)

    elif args[0]=="distributions":
        max_extents, gyr_extents, pops = distributions_of_time(init_N, N, mu, n_sim)

        ani_fig = plt.figure()
        ani_fig.suptitle(r'Distributions for $R_{m}(t)$, $R_{g}(t)$, and $N(t)$',fontsize=14, fontweight='bold')
        #f, (pop_ax,rmax_ax,rgyr_ax) = plt.subplots(1,3)
        #pop_ax.set_xlabel(r'N(t)')
        #pop_ax.set_ylabel(r'Probability')
        #rmax_ax.set_xlabel(r'R_{m}(t)')
        #rgyr_ax.set_xlabel(r'R_{g}(t)')
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Chris Dock'),bitrate=1800)
        ims = []
        popc = rc()
        rmc = rc()
        rgc = rc()
        for g in range(1, len(max_extents)):
            print g
            pop_hist, pop_edges = np.histogram(np.array(pops[g]),100,normed=True)
            pop_edges = [edge + (pop_edges[1]-pop_edges[0])/2. for edge in pop_edges][:-1]
            #im1 = plt.scatter(pop_edges,pop_hist,color=popc,marker='o')
            #pn, pb, pp = pop_ax.hist(pops[g], 100, facecolor=rc())
            #rmn,rmb,rmp = rmax_ax.hist(max_extents[g],100,facecolor=rc())
            #irgn,rgb,rgp = rgyr_ax.hist(gyr_extents[g],100,facecolor=rc())
            ims.append((plt.scatter(pop_edges,pop_hist,color=popc,marker='o'),))
        im_ani = animation.ArtistAnimation(ani_fig,ims, interval=50, repeat_delay=3000,blit=True)
        im_ani.save('ouputs/distribution_animation.mp4',writer=writer)


