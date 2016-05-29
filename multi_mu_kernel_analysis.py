from universal import *
from growth_simulator import *
from outbreak_splitter import *
from kernel_analysis import *

include_secondaries = False

def expectation_of_kernels(N, mus, n_sim, incl_secs = False, ug = True, mpop=-1):
    kernels = {}
    for mu in mus:
        pairs =[]
        for i in range(0, n_sim):
            print i
            simulation_results = c_outbreak(N, mu)
            r_of_t = simulation_results["gyr_r"]
            generations = simulation_results["gens"]
            primary_kernel = list(zip(*invert_to_kernel_convolution(r_of_t)))
            pairs.extend(primary_kernel)
            if incl_secs:
                secondary_r_of_ts = get_secondaries(generations)[1]
                secondary_count=0
                for s_r_of_t in secondary_r_of_ts.values():
                    secondary_kernel = list(zip(*invert_to_kernel_convolution(s_r_of_t)))
                    secondary_count += len(secondary_kernel)
                    pairs.extend(secondary_kernel)
        pairs.sort(key = lambda p: p[0])
        kernels[mu] = zip(*pairs)
    return kernels

def kernels_of_expectations(N, mus, n_sim, incl_secs = False, ug = True, mpop=-1):
    kernels = {}
    for mu in mus:
        r_of_ts = []
        for i in range(0, n_sim):
            print "i = {0}".format(i)
            simulation_results = c_outbreak(N, mu)
            r_of_ts.append(simulation_results["gyr_r"])
            if incl_secs:
                secondary_r_of_ts = get_secondaries(generations)[1]
                secondary_count = 0
                for s_r_of_t in secondary_r_of_ts.values():
                    r_of_ts.append(s_r_of_t)
                    secondary_count+=1
        av_r_of_t = {k: mean([r_of_t[k] for r_of_t in r_of_ts]) for k in r_of_ts[0].keys()}
        kernels[mu] = invert_to_kernel_convolution(av_r_of_t)
    return kernels





def mu_retrieval(actual_mu, kernel):
    ls = np.asarray(kernel[0], dtype = 'float')
    gs = np.asarray(kernel[1], dtype = 'float')
    log_ls = np.log(ls)
    log_gs = np.log(gs)
    coefficients = np.polyfit(log_ls,log_gs,1)
    print "Actual mu = " + str(actual_mu)
    mu_approx = -(coefficients[0]+d)
    print "Approximated mu = " + str(mu_approx)
    print "Relative error = " + str(abs(actual_mu-mu_approx)/actual_mu)
    return mu_approx, coefficients, log_ls, log_gs, ls, gs






if __name__ == '__main__':
    N = 50
    n_sim = 1000
    mus = [1.6, 1.7,1.8,1.9,2.0,2.1,2.2]
    kernels = expectation_of_kernels(N, mus, n_sim)
    kernel_fig = plt.figure()
    kernel_fig.suptitle(r'Approximated Jump Kernel for simulation, $n_s={1}$, $[\mu]={0}$'.format(mus,n_sim))
    kernel_ax = kernel_fig.add_subplot(111)
    kernel_fig.subplots_adjust(top=.9)
    kernel_ax.set_yscale('log')
    kernel_ax.set_xscale('log')
    kernel_ax.set_xlabel(r'$\log(l)$')
    kernel_ax.set_ylabel(r'$\approx \log(G(l))$')
    legend_data = [[],[]]
    c_i = 0
    for actual_mu, kernel in kernels.items():
        mu_approx,coefficients,log_ls,log_gs,ls,gs = mu_retrieval(actual_mu, kernel)

        kernel_ax.plot(*kernel, color = my_colors[c_i%len(my_colors)], alpha=.3)
        legend_data[1].append(r'Actual $\mu$: {0}, Fitted $\mu$: {1}'.format(actual_mu,mu_approx))
        polynomial = np.poly1d(coefficients)
        fit_log_gs = polynomial(log_ls)
        plot_pointer, = kernel_ax.plot(ls,np.exp(fit_log_gs), color = my_colors[c_i%len(my_colors)],alpha=1.)
        c_i+=1
        legend_data[0].append(plot_pointer)

    plt.legend(tuple(legend_data[0]), tuple(legend_data[1]), loc='lower left', ncol=1, fontsize=8)
    kernel_fig.savefig("outputs/multi_mu_kernel_plot_N{0}_nsim{1}.png".format(N,n_sim), dpi=400)
    plt.clf()


