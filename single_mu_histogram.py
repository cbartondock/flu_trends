from universal import *
from growth_simulator import *
from multiple_sims import *
from kernel_analysis import *

def get_all_mus(mean_rs):
    mus=[]
    for mean_r in mean_rs:
        mus.append(mu_retrieval(invert_to_kernel_convolution(mean_r["mean_r"]))[0])
    return mus


if __name__ == '__main__':
    mu = 2.0
    mp= int(10**4)
    n_sim = 10000
    mean_rs = many_sims([mu],mp,seed_lattice(1),n_sim, ["mean_r","params"])
    mu_estimates = get_all_mus(mean_rs)

    mu_fig = plt.figure()
    mu_fig.suptitle(r'Histogram of estimated $\mu$ values for $\mu={0}$'.format(mu))
    mu_ax = mu_fig.add_subplot(111)
    mu_fig.subplots_adjust(top=.9)
    mu_ax.set_xlabel(r'$\mu_{\mbox{approx}}$')
    mu_ax.set_ylabel(r'$P$')
    plt.hist(np.array(mu_estimates), 100,normed=1,facecolor=rc(),alpha=.8)
    mu_fig.savefig("outputs/mu_hist_t"+str(round(time.time()))+"_nsim{0}_mu{1}.png".format(n_sim,mu), dpi=400)
    plt.clf()
    plt.close(mu_fig)

