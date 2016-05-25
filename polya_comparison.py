from growth_simulator import *
from universal import *

def compare_methods(N, mu, n_sim):
    gyr_r = {g: 0 for g in range(0,N)}
    polya_gyr_r = {g: 0 for g in range(0,N)}
    pop = {g: 0 for g in range(0,N)}
    polya_pop = {g: 0 for g in range(0,N)}
    for i in range(0, n_sim):
        data = simulate_outbreak(N, mu)
        polya_data = polya_outbreak(N, mu)
        gyr_r = {g: gyr_r[g] + data["gyr_r"][g] for g in range(0,N)}
        polya_gyr_r = {g: polya_gyr_r[g] + polya_data["gyr_r"][g] for g in range(0,N)}
        pop = {g: pop[g] + data["pop"][g] for g in range(0,N)}
        polya_pop = {g: polya_pop[g] + polya_data["pop"][g] for g in range(0,N)}
        print data["gyr_r"]
        print polya_data["gyr_r"]
    gyr_r = {g: gyr_r[g]/float(n_sim) for g in range(0,N)}
    polya_gyr_r = {g: polya_gyr_r[g]/float(n_sim) for g in range(0,N)}
    pop = {g: pop[g]/float(n_sim) for g in range(0,N)}
    polya_pop = {g: polya_pop[g]/float(n_sim) for g in range(0,N)}
    return gyr_r, polya_gyr_r, pop, polya_pop


if __name__ == '__main__':
    N = 15
    mu = 1.8
    n_sim = 20
    gyr_r, polya_gyr_r, pop, polya_pop = compare_methods(N, mu, n_sim)
    print "Plotting Polya vs. Normal"
    plt.suptitle(r'Comparison with Polya Dynamics over {0} generations, $\mu={1}$'.format(N, mu),  fontweight='bold')
    f, (ax1, ax2) = plt.subplots(1, 2)
    ppplot = ax2.scatter(list(range(0,N)), [polya_pop[g] for g in range(0,N)], color=rc())
    pplot = ax2.scatter(list(range(0,N)), [pop[g] for g in range(0,N)], color=rc())
    gplot = ax1.scatter(list(range(0,N)),[gyr_r[g] for g in range(0,N)], color=rc())
    pgplot = ax1.scatter(list(range(0,N)),[polya_gyr_r[g] for g in range(0,N)], color=rc())
    ax1.set_xlabel(r'Generation')
    ax2.set_xlabel(r'Generation')
    ax1.set_ylabel(r'Gyration Radius')
    ax2.set_ylabel(r'Population')
    ax1.set_ylim([0,max(max(gyr_r.values()),max(polya_gyr_r.values()))])
    ax2.set_ylim([0,max(max(pop.values()),max(polya_pop.values()))])
    ax1.legend(handles = [gplot, pgplot], labels = ["Normal Simulation", "Polya Simulation"])
    ax2.legend(handles = [pplot, ppplot], labels = ["Normal Simulation", "Polya Simulation"])
    plt.savefig("outputs/comparison_plot_N{0}_mu{1}.png".format(N,mu),dpi=400)

