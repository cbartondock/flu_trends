from multiple_sims import *


def radial_mean_and_dev(multiple_sims_data):
    N = min([len(data["gens"]) for data in multiple_sims_data])
    max_r_av = [0 for t in range(0, N)]
    mean_r_av = [0 for t in range(0, N)]
    max_r_dev = [0 for t in range(0, N)]
    mean_r_dev = [0 for t in range(0, N)]
    for t in range(0,N):
        N_t = 0
        for data in multiple_sims_data:
            if t<len(data["gens"]):
                N_t+=1
                max_r_av[t]+=data["max_r"][t]
                mean_r_av[t]+=data["mean_r"][t]
                max_r_dev[t]+=data["max_r"][t]**2
                mean_r_dev[t]+=data["mean_r"][t]**2
        max_r_av[t]/=float(N_t)
        mean_r_av[t]/=float(N_t)
        max_r_dev[t]= (max_r_dev[t]/float(N_t) - max_r_av[t]**2)**.5
        mean_r_dev[t]= (mean_r_dev[t]/float(N_t) - mean_r_av[t]**2)**.5

    return max_r_av, mean_r_av, max_r_dev, mean_r_dev, N



if __name__ == '__main__':
    n_sim = 1000
    mp=10**4
    mu = 1.8

    max_r, mean_r, max_r_dev, mean_r_dev, N = radial_mean_and_dev(many_sims([mu], mp,seed_lattice(1), n_sim))
    print max_r_dev
    print mean_r_dev
    scaling = get_crossover_scaling(mu)
    print "Plotting Radii"
    radii_fig = plt.figure()
    radii_fig.suptitle(r'Averaged radial growth with max pop. $10^{0}$, $\mu={1}$'.format(tenexp(mp), mu),  fontweight='bold')
    radii_ax = radii_fig.add_subplot(111)
    radii_fig.subplots_adjust(top=.9)
    meanplot = radii_ax.scatter(range(0,N),mean_r, color=rc(False))
    radii_ax.errorbar(list(range(0,N)),mean_r,yerr=mean_r_dev,color=rc())
    maxplot = radii_ax.scatter(list(range(0,N)),max_r, color=rc(False))
    radii_ax.errorbar(list(range(0,N)),max_r,yerr=mean_r_dev,color=rc())
    fpatch = mpatches.Patch(color=rc(False))
    fitplot = radii_ax.plot([scaling(g) for g in range(0,N)],c=rc())
    radii_ax.set_xlabel(r'Generation')
    radii_ax.set_ylabel(r'Distance in Demes')
    radii_ax.legend(handles=[meanplot,maxplot,fpatch],labels=[r'Mean Radius', r'Maximum Radius', r'Crossover Prediction'], loc='upper left')
    radii_fig.savefig("outputs/average_radial_plot_mp{0}_mu{1}.png".format(tenexp(mp),mu),dpi=400)


