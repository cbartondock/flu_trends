from growth_simulator import *
from universal import *



def rad_expectations(N, mu, n_sim):
    max_r_av = {t: 0 for t in range(0, N)}
    gyr_r_av = {t: 0 for t in range(0, N)}
    for i in range(0, n_sim):
        print i
        data = c_outbreak(N, mu)
        print "stupid data: " + str(data["max_r"][0])
        max_r_av = {t: max_r_av[t] + data["max_r"][t] for t in range(0,N)}
        gyr_r_av = {t: gyr_r_av[t] + data["gyr_r"][t] for t in range(0,N)}
    max_r_av = {t: max_r_av[t]/float(n_sim) for t in range(0,N)}
    gyr_r_av = {t: gyr_r_av[t]/float(n_sim) for t in range(0,N)}

    return max_r_av, gyr_r_av



if __name__ == '__main__':
    n_sim = 100
    N = 100
    mu = 1.8

    max_r, gyr_r = rad_expectations(N, mu, n_sim)
    scaling = get_crossover_scaling(mu)
    print "Plotting Radii"
    radii_fig = plt.figure()
    radii_fig.suptitle(r'Averaged radial growth over {0} generations, $\mu={1}$'.format(N, mu),  fontweight='bold')
    radii_ax = radii_fig.add_subplot(111)
    radii_fig.subplots_adjust(top=.9)
    gyrplot = radii_ax.scatter(list(range(0,N)),[gyr_r[g] for g in range(0,N)], color=rc())
    maxplot = radii_ax.scatter(list(range(0,N)),[max_r[g] for g in range(0,N)], color=rc())
    fc = rc()
    fpatch = mpatches.Patch(color=fc)
    fitplot = radii_ax.plot([scaling(g) for g in range(0,N)],c=fc)
    radii_ax.set_xlabel(r'Generation')
    radii_ax.set_ylabel(r'Radius')
    radii_ax.legend(handles=[gyrplot,maxplot,fpatch],labels=[r'Gyration Radius', r'Maximum Radius', r'Crossover Prediction'], loc='upper left')
    radii_fig.savefig("outputs/average_radial_plot_N{0}_mu{1}.png".format(N,mu),dpi=400)


