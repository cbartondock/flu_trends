from universal import *
from growth_simulator import *
from multiple_sims import *
from outbreak_splitter import *
from kernel_analysis import *

def kernels_of_expectations(multiple_sims_data):
    mus = [sim["params"]["mu"] for sim in multiple_sims_data]
    N = min([len(sim["gens"]) for sim in multiple_sims_data])
    r_of_ts = {mu: [] for mu in mus}
    kernels = {}
    max_t=0
    for data in multiple_sims_data:
        r_of_ts[data["params"]["mu"]].append(data["mean_r"])
        if len(data["gens"]) > max_t:
            max_t = len(data["gens"])
    for mu in mus:
        av_r_of_t = {t: mean([r_of_t[t] for r_of_t in r_of_ts[mu] if t <N]) for t in range(0, max_t)}
        kernels[mu] = invert_to_kernel_convolution(av_r_of_t)
    return kernels



#Unclear if Least Squares is the best approach here
def mu_retrieval(kernel):
    ls = np.asarray(kernel[0], dtype = 'float')
    gs = np.asarray(kernel[1], dtype = 'float')
    log_ls = np.log(ls)
    log_gs = np.log(gs)
    coefficients = np.polyfit(log_ls,log_gs,1)
    mu_approx = -(coefficients[0]+d)
    return mu_approx, coefficients, log_ls, log_gs, ls, gs






if __name__ == '__main__':
    mp= int(10**4)
    n_sim = 1000
    mus = [1.6,1.8,2.0,2.2]
    #multiple_sims_data = many_sims(mus,mp,seed_lattice(1),n_sim)
    multiple_sims_data = pickle.load(open("data_outputs/1.pkl",'r'))
    kernels = kernels_of_expectations(multiple_sims_data)
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
        print "Actual mu: " + str(actual_mu)
        mu_approx,coefficients,log_ls,log_gs,ls,gs = mu_retrieval(kernel)
        print "Approx mu: " + str(mu_approx)

        print "Relative error = " + str(abs(actual_mu-mu_approx)/actual_mu)
        kernel_ax.plot(*kernel, color = my_colors[c_i%len(my_colors)], alpha=.3)
        legend_data[1].append(r'Actual $\mu$: {0}, Fitted $\mu$: {1}'.format(actual_mu,mu_approx))
        polynomial = np.poly1d(coefficients)
        fit_log_gs = polynomial(log_ls)
        plot_pointer, = kernel_ax.plot(ls,np.exp(fit_log_gs), color = my_colors[c_i%len(my_colors)],alpha=1.)
        c_i+=1
        legend_data[0].append(plot_pointer)

    plt.legend(tuple(legend_data[0]), tuple(legend_data[1]), loc='lower left', ncol=1, fontsize=8)
    kernel_fig.savefig("outputs/multi_mu_kernel_plot_mp{0}_nsim{1}_mus{2}.png".format(tenexp(mp),n_sim,"-".join([str(int(10*mu)) for mu in mus])), dpi=400)
    plt.clf()


