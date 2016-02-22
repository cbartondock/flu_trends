from universal import *
from growth_simulator import simulate_outbreak
from kernel_analysis import *

N = 20
mus = [2.1, 2.3, 2.5, 2.7, 2.9]
L = 1000000000
C = 1
n_sim = 50

kernels = {}
for mu in mus:
    radial_results = []
    for i in range(0, n_sim):
        radial_results.append(simulate_outbreak(d, N, mu, L, C)[2])
    kernels[mu] = mean(map(lambda rt: invert_to_kernel(rt, N), radial_results))
    print list(av_rad.items())
#    plt.scatter(*zip(*list(av_rad.items())))
#plt.savefig('multi_mu_kernel_test.png')
#plt.clf()

kernel_fig = plt.figure()
kernel_fig.suptitle(r'Approximated Jump Kernel for simulation, $\mu={0}$, $n_s={1}$'.format(mu,n_sim))
kernel_ax = kernel_fig.add_subplot(111)
kernel_fig.subplots_adjust(top=.9)
kernel_ax.set_yscale('log')
kernel_ax.set_xscale('log')
kernel_ax.set_xlabel(r'$\log(l)$')
kernel_ax.set_ylabel(r'$\approx \log(G(l))$')
legend_data = [[],[]]
for mu, kernel in kernels.items():
    kernel_ax.plot(*kernel, alpha=.5)
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
    plot_pointer, = kernel_ax.plot(ls,np.exp(fit_log_gs))
    legend_data[0].append(plot_pointer)
plt.legend(tuple(legend_data[0]), tuple(legend_data[1]), loc='upper left', ncol=1, fontsize=8)
kernel_fig.savefig("outputs/multi_mu_kernel_plot_N{0}_nsim{1}.png".format(N,n_sim), dpi=400)
plt.clf()

