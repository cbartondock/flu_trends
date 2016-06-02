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
        max_fluct[g] = (mean([(max_extent - max_mean[g])**2 for max_extent in max_extents[g]])**.5)/max_mean[g]
        gyr_fluct[g] = (mean([(gyr_extent -gyr_mean[g])**2 for gyr_extent in gyr_extents[g]])**.5)/gyr_mean[g]
        pop_fluct[g] = (mean([(pop - pop_mean[g])**2 for pop in pops[g]])**.5)/pop_mean[g]
    return max_fluct, gyr_fluct, pop_fluct

def average_over_initials(M_pop,N, mu, n_sim_per_seed,n_seeds_per_size):
    term_popfluct = {}
    term_rgfluct = {}
    term_rmfluct = {}
    term_popmean = {}
    term_rgmean = {}
    term_rmmean = {}
    for mp in range(1,M_pop+1):
        max_flucts = []
        gyr_flucts = []
        pop_flucts = []
        max_means = []
        gyr_means = []
        pop_means = []
        print "mp = " +str(mp)
        for i in range(0,n_seeds_per_size):
            seeds = [[deme[0], deme[1], 0] for deme in c_outbreak(0,mu,ug=False,mp=mp)["infected"]]
            term_infected_states = []
            print "i = " +str(i)
            for j in range(0, n_sim_per_seed):
                infected = c_outbreak(N,mu, seeds=seeds)["infected"]
                term_infected_states.append(infected)
            max_extents = [max_rad(mean([p[0] for p in state]),
                mean([p[1] for p in state]),state) for state in term_infected_states]
            gyr_extents = [gyr_rad(mean([p[0] for p in state]),
                mean([p[1] for p in state]),state) for state in term_infected_states]
            pops = [len(state) for state in term_infected_states]
            max_mean, gyr_mean, pop_mean = mean(max_extents), mean(gyr_extents), mean(pops)
            max_means.append(max_mean)
            gyr_means.append(gyr_mean)
            pop_means.append(pop_mean)
            max_flucts.append((mean([(max_extent - max_mean)**2 for max_extent in max_extents])**.5)/max_mean)
            gyr_flucts.append((mean([(gyr_extent -gyr_mean)**2 for gyr_extent in gyr_extents])**.5)/gyr_mean)
            pop_flucts.append((mean([(pop - pop_mean)**2 for pop in pops])**.5)/pop_mean)
        term_popfluct[mp] = mean(pop_flucts)
        term_rgfluct[mp] = mean(gyr_flucts)
        term_rmfluct[mp] = mean(max_flucts)
        term_popmean[mp] = mean(pop_means)
        term_rgmean[mp] = mean(gyr_means)
        term_rmmean[mp] = mean(max_means)
    return term_popfluct,term_rgfluct,term_rmfluct,term_popmean,term_rgmean,term_rmmean


if __name__ == '__main__':
    init_N = 10
    N = 200
    mu = 1.8
    n_sim = 100

    args = sys.argv[1:]
    if len(args)==0 or args[0] == "fluctuations":
        max_f, gyr_f, pop_f = fluctuation_of_time(init_N,N, mu, n_sim)
        f, (fluct_ax1,fluct_ax2)  = plt.subplots(1,2)
        f.suptitle(r'Averaged Fluctuations over {0} generations with {2} seed generations, $\mu={1}$'.format(N, mu, init_N),  fontweight='bold',fontsize=14)
        gyrplot = fluct_ax1.scatter(list(range(0,N)),[gyr_f[g] for g in range(0,N)], color=rc())
        maxplot = fluct_ax1.scatter(list(range(0,N)),[max_f[g] for g in range(0,N)], color=rc())
        popplot = fluct_ax2.scatter(list(range(0,N)),[pop_f[g] for g in range(0,N)], color=rc())
        fluct_ax1.set_xlabel(r'Generation')
        fluct_ax1.set_ylabel(r'Fluctuation')
        fluct_ax1.legend(handles=[gyrplot,maxplot],labels=[r'$R_{g}(t)$ Fluctuation', r'$R_{m}(t)$ Fluctuation'], loc='upper left')
        fluct_ax2.set_xlabel(r'Generation')
        fluct_ax2.legend(handles=[popplot],labels=[r'$N(t)$ Fluctuation'])
        f.savefig("outputs/average_fluctuation_plot_N{0}_mu{1}_Ns{2}.png".format(N,mu,init_N),dpi=400)

    elif args[0] == "terminals":
        M_pop = 25
        N = 15
        mu = 1.8
        n_sim_per_seed=210
        n_seeds_per_size=50
        tpf,tgf,tmf,tpm,tgm,tmm = average_over_initials(M_pop,N,mu,n_sim_per_seed,n_seeds_per_size)
        f, (trf_ax,tpf_ax)= plt.subplots(1, 2)
        f.suptitle(r'Asymptotic Fluctuations (after {1} generations) vs. Seed Size for $mu={0}$'.format(mu,N),fontweight='bold',fontsize=14)
        popplot = tpf_ax.scatter(list(range(1,M_pop+1)),[tpf[mp] for mp in range(1,M_pop+1)],color=rc())
        gyrplot = trf_ax.scatter(list(range(1,M_pop+1)),[tgf[mp] for mp in range(1,M_pop+1)],color=rc())
        maxplot = trf_ax.scatter(list(range(1,M_pop+1)),[tmf[mp] for mp in range(1,M_pop+1)],color=rc())
        trf_ax.legend(handles=[gyrplot,maxplot],labels=[r'$R_{g}^\infty$ Fluctuation', r'$R_{m}^\infty$ Fluctuation'], loc='upper left')
        tpf_ax.legend(handles=[popplot],labels=[r'$N^\infty$ Fluctuation'])
        trf_ax.set_xlabel(r'Seed Size')
        tpf_ax.set_xlabel(r'Seed Size')
        trf_ax.set_ylabel(r'Fluctuation as $t\rightarrow\infty$')
        f.savefig("outputs/terminal_fluctuation_plot_mu{0}_N{1}.png".format(mu,N),dpi=400)

    elif args[0]=="distributions":
        max_extents, gyr_extents, pops = distributions_of_time(init_N, N, mu, n_sim)

        ani_fig, (pop_ax,rmax_ax,rgyr_ax) = plt.subplots(1, 3)
        ani_fig.suptitle(r'Distributions for $R_{m}(t)$, $R_{g}(t)$, and $N(t)$',fontsize=14, fontweight='bold')
        plt.locator_params(axis='x',nbins=4)
        pop_ax.set_xlabel(r'$N(t)$')
        pop_ax.set_ylabel(r'Probability')
        rmax_ax.set_xlabel(r'$R_{m}(t)$')
        rgyr_ax.set_xlabel(r'$R_{g}(t)$')
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Chris Dock'), bitrate=1800)
        popc = rc()
        rmc = rc()
        rgc = rc()
        popline = pop_ax.plot([],[],color=popc,marker='o',lw=0)[0]
        rmline = rmax_ax.plot([],[],color=rmc,marker='o',lw=0)[0]
        rgline = rgyr_ax.plot([],[],color=rgc,marker='o',lw=0)[0]
        def init():
            popline.set_data([],[])
            rmline.set_data([],[])
            rgline.set_data([],[])
            return [popline, rmline, rgline]
        def animate(i):
            g=i+1
            print "g is "+str(g)
            pop_weights = np.ones_like(pops[g])/float(len(pops[g]))
            pop_hist, pop_edges = np.histogram(np.array(pops[g]),100,normed=0,weights=pop_weights)
            pop_edges = [edge + (pop_edges[1]-pop_edges[0])/2. for edge in pop_edges][:-1]
            popline.set_data(pop_edges,pop_hist)
            pop_ax.set_xlim([int(min(pop_edges))-2,int(max(pop_edges))+2])
            pop_ax.set_ylim([0,max(pop_hist)*1.1])
            start, end = pop_ax.get_xlim()
            pop_ax.xaxis.set_ticks(np.arange(start,end,(end-start)//3))
            rm_weights = np.ones_like(max_extents[g])/float(len(max_extents[g]))
            rm_hist, rm_edges = np.histogram(np.array(max_extents[g]),100,normed=0,weights=rm_weights)
            rm_edges = [edge + (rm_edges[1]-rm_edges[0])/2. for edge in rm_edges][:-1]
            rmline.set_data(rm_edges,rm_hist)
            rmax_ax.set_xlim([int(min(rm_edges))-2,int(max(rm_edges))+2])
            rmax_ax.set_ylim([0,max(rm_hist)*1.1])
            start, end = rmax_ax.get_xlim()
            rmax_ax.xaxis.set_ticks(np.arange(start,end,(end-start)//3))
            rg_weights = np.ones_like(gyr_extents[g])/float(len(gyr_extents[g]))
            rg_hist, rg_edges = np.histogram(np.array(gyr_extents[g]),100,normed=0,weights=rg_weights)
            rg_edges = [edge + (rg_edges[1]-rg_edges[0])/2. for edge in rg_edges][:-1]
            rgline.set_data(rg_edges,rg_hist)
            rgyr_ax.set_xlim([int(min(rg_edges))-2,int(max(rg_edges))+2])
            rgyr_ax.set_ylim([0,max(rg_hist)*1.1])
            start, end = rgyr_ax.get_xlim()
            rgyr_ax.xaxis.set_ticks(np.arange(start,end,(end-start)//3))
            return [popline, rmline, rgline]
        print "Beginning Animation"
        anim = animation.FuncAnimation(ani_fig,animate,init_func=init,frames=len(pops)-1,interval=20,blit=True)
        anim.save('outputs/dist_animation_N{0}_mu_{1}.mp4'.format(N,mu),writer=writer,dpi=500)
