from universal import *
from growth_simulator import simulate_outbreak
from outbreak_splitter import *
from kernel_analysis import *

N = 10
mus = [1.9,2.0,2.1]
L = 1000000000
C = 1
n_sim = 3
max_pop = 10**5;
kernels = {}
for mu in mus:
    pairs =[]
    for i in range(0, n_sim):
        simulation_results = simulate_outbreak(d, N, mu, L, C, False, max_pop)
        r_of_t = simulation_results[2]
        generations = simulation_results[1]
        secondary_r_of_ts = get_secondaries(generations)[1]
        primary_kernel = list(zip(*invert_to_kernel(r_of_t)))
        pairs.extend(primary_kernel)
        secondary_count=0
        for s_node, s_r_of_t in secondary_r_of_ts.items():
            secondary_kernel = list(zip(*invert_to_kernel(s_r_of_t)))
            secondary_count += len(secondary_kernel)
            pairs.extend(secondary_kernel)
        print "Secondary outbreaks got us an extra {0} kernel points for mu={1}".format(secondary_count, mu)
    pairs.sort(key = lambda p: p[0])
    kernels[mu] = zip(*pairs)
    #print kernels[mu]

kernel_fig = plt.figure()
kernel_fig.suptitle(r'Approximated Jump Kernel for simulation, $n_s={1}$'.format(mu,n_sim))
kernel_ax = kernel_fig.add_subplot(111)
kernel_fig.subplots_adjust(top=.9)
kernel_ax.set_yscale('log')
kernel_ax.set_xscale('log')
kernel_ax.set_xlabel(r'$\log(l)$')
kernel_ax.set_ylabel(r'$\approx \log(G(l))$')
legend_data = [[],[]]
c_i = 0
for mu, kernel in kernels.items():
    kernel_ax.plot(*kernel, color = my_colors[c_i%len(my_colors)], alpha=.3)
    ls = np.asarray(kernel[0], dtype = 'float')
    gs = np.asarray(kernel[1], dtype = 'float')
    log_ls = np.log(ls)
    log_gs = np.log(gs)
    coefficients = np.polyfit(log_ls,log_gs,1)
    print "Actual mu = " + str(mu)
    mu_approx = -(coefficients[0]+d)
    print "Approximated mu = " + str(mu_approx)
    print "Relative error = " + str(abs(mu-mu_approx)/mu)
    legend_data[1].append(r'Actual $\mu$: {0}, Fitted $\mu$: {1}'.format(mu,mu_approx))
    polynomial = np.poly1d(coefficients)
    fit_log_gs = polynomial(log_ls)
    plot_pointer, = kernel_ax.plot(ls,np.exp(fit_log_gs), color = my_colors[c_i%len(my_colors)],alpha=1.)
    c_i+=1
    legend_data[0].append(plot_pointer)
plt.legend(tuple(legend_data[0]), tuple(legend_data[1]), loc='lower left', ncol=1, fontsize=8)
kernel_fig.savefig("outputs/multi_mu_kernel_plot_N{0}_nsim{1}.png".format(N,n_sim), dpi=400)
plt.clf()

