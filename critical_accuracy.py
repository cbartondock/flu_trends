from universal import *
from growth_simulator import *
from multiple_sims import *
from scipy import stats
#def get_r2s(mus,n_sim):


if __name__ == '__main__':
    n_sim=1000
    mp=10**4
    mus = np.arange(1.2,3.5,.1)
    mean_rs = many_sims(mus, mp,seed_lattice(1),n_sim, ["mean_r","params"])
    crit_scaling=get_critical_scaling()
    fitfunc = lambda scaling: np.vectorize(lambda t, *p: p[0]*(scaling(t)-scaling(0)))
    N = min([len(mean_r["mean_r"]) for mean_r in mean_rs])
    r_of_ts = {mu: [] for mu in mus}
    max_t=0
    mu_rs=[]
    for mean_r in mean_rs:
        r_of_ts[mean_r["params"]["mu"]].append(mean_r["mean_r"])
        if len(mean_r["mean_r"]) > max_t:
            max_t= len(mean_r["mean_r"])
    for mu in mus:
        print "mu: " + str(mu)
        av_r_of_t = zip(*[(t, mean([r_of_t[t] for r_of_t in r_of_ts[mu] if t <N])) for t in range(0, max_t)])
        #p_crit, cov_crit = curve_fit(fitfunc(crit_scaling), av_r_of_t[0], av_r_of_t[1],p0=(1,))
        s, i, r, p, se = stats.linregress(av_r_of_t[1],fitfunc(crit_scaling)(av_r_of_t[0],1))
        mu_rs.append((mu, r**2))
    print mu_rs
    mu_rs = zip(*mu_rs)
    murs_fig = plt.figure()
    murs_fig.suptitle(r'$R^2$ between scaled critical case and average $l(t)$ for given $\mu$')
    murs_ax = murs_fig.add_subplot(111)
    murs_fig.subplots_adjust(top=.9)
    murs_ax.set_xlabel(r'$\mu$')
    murs_ax.set_ylabel(r'$R^2$')
    murs_ax.plot(mu_rs[0],mu_rs[1], color = rc())
    murs_fig.savefig("outputs/murs_plot_t"+str(round(time.time()))+"_nsim{0}.png".format(n_sim), dpi=400)
    plt.clf()
    plt.close(murs_fig)







