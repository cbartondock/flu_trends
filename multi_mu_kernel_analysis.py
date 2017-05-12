from universal import *
from growth_simulator import *
from multiple_sims import *
from kernel_analysis import *

def kernels_of_expectations(mus, mean_rs):
    N = min([len(mean_r["mean_r"]) for mean_r in mean_rs])
    r_of_ts = {mu: [] for mu in mus}
    kernels = {}
    max_t=0
    for mean_r in mean_rs:
        r_of_ts[mean_r["params"]["mu"]].append(mean_r["mean_r"])
        if len(mean_r["mean_r"]) > max_t:
            max_t= len(mean_r["mean_r"])
    for mu in mus:
        print "mu: " + str(mu)
        av_r_of_t = {t: mean([r_of_t[t] for r_of_t in r_of_ts[mu] if t <N]) for t in range(0, max_t)}
        kernels[mu] = invert_to_kernel_convolution(av_r_of_t)
    return kernels





#Log Likeliness?




if __name__ == '__main__':

    #multiple_sims_data = pickle.load(open("data_outputs/1.pkl",'r'))
    mus=[1.6,1.8,2.0,2.2,2.4]
    #mus=[2.1]
    mp= int(10**5)
    n_sim = 1000
    mean_rs = many_sims(mus,mp,seed_lattice(1),n_sim, ["mean_r","params"])
    print "finished sims"
    kernels = kernels_of_expectations(mus, mean_rs)
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


