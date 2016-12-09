from frequency_analysis import *
from multiple_sims import *

def var_max_freqs(multiple_sims_data):
    N = min([len(data["gens"]) for data in multiple_sims_data])
    av_max_freqs = {g: 0 for g in range(0,N)}
    dev_max_freqs = {g: 0 for g in range(0,N)}
    for data in multiple_sims_data:
        freqs = get_frequency_functions(data)
        for j in range(0,N):
            maxfreq=max(freqs[j].values)
            av_max_freqs[j]+=maxfreq
            dev_max_freqs[j]+=maxfreq**2
    n_sims =len(multiple_sims_data)
    m

max_freqs = {g: [] for g in range(0,N)}
        for i in range(0, n_sims):
            print i
            seeds = seed_lattice(n_seeds)
            data = c_outbreak(N,mu,seeds=seeds,choice_f=choice_f)
            freqs = get_frequency_functions(data)
            for j in range(0,N):
                max_freqs[j].append(max(freqs[j].values()))
        mean_max_freqs = [mean(max_freqs[g]) for g in range(0,N)]
        var_max_freqs = [mean([(max_freq-mean_max_freqs[g])**2 for max_freq in max_freqs[g]]) for g in range(0,N)]
        f, (mean_ax, var_ax) = plt.subplots(1, 2)
        f.suptitle(r"Max Frequency Mean and Variance for $\mu={0}$ with {1} types".format(mu,num_opts))
        mean_plot = mean_ax.plot(mean_max_freqs,c=rc())
        var_plot = var_ax.plot(var_max_freqs,c =rc())
        mean_ax.set_ylabel(r'$f$')
        mean_ax.set_xlabel(r'Generation')
        var_ax.set_xlabel(r'Generation')
        var_ax.text(.1,.9,r'Variance',transform=var_ax.transAxes)
        mean_ax.text(.1,.9,r'Mean',transform=mean_ax.transAxes)
        f.savefig("outputs/meanvar_freq_plot_N{0}_mu{1}_no{2}.png".format(N,mu,num_opts),dpi=500)

