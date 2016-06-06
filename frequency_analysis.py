from universal import *
from growth_simulator import *
from standard_plotters import *

#m*n_attr = num_seeds
def even_choice_f(n_attrs, m):
    opts = [i for j in range(0, m) for i in range(0, n_attrs)]
    shuffle(opts)
    index = 0
    nonlocals = {"opts":opts,"index":index}
    def choice_f(d):
        result = nonlocals["opts"][nonlocals["index"]]
        nonlocals["index"] = (nonlocals["index"]+1)%len(nonlocals["opts"])
        return result
    return choice_f

def get_frequency_functions(data):
    gens = data["gens"]
    attr_dict = data["attr"]

    totals = Counter()
    frequencies= {0: Counter()}
    totals[0] = len(gens[0])
    for seed in gens[0]:
        frequencies[0][attr_dict[(seed[0],seed[1])]]+=1

    for i in range(1,len(gens)):
        frequencies[i] = Counter()
        for value in attr_dict.values():
            frequencies[i][value] = frequencies[i-1][value]
        for deme in gens[i]:
            frequencies[i][attr_dict[(deme[0],deme[1])]]+=1
        totals[i]=totals[i-1] + len(gens[i])
    for i in range(0, len(gens)):
        frequencies[i] = {key: value/float(totals[i]) for key,value in frequencies[i].items()}
    return frequencies

if __name__=="__main__":
    N=200
    mu=1.8
    n_seeds=10
    num_opts=5
    choice_f = even_choice_f(num_opts,n_seeds//num_opts)
    n_sims = 50
    args = sys.argv[1:]
    if len(args)==0 or args[0]=="frequencies":
        seeds = seed_lattice(n_seeds)
        data = c_outbreak(N,mu, seeds=seeds,choice_f=choice_f)
        freqs = get_frequency_functions(data)
        f = plt.figure()
        f.suptitle(r'Type Frequency vs. Time for $N={0}$, $\mu={1}$'.format(N,mu))
        ax = f.add_subplot(111)
        ax.set_xlabel(r'Generation');
        ax.set_ylabel(r'$f$')
        handles=[]
        for j in range(0, num_opts):
            fc=rc()
            ax.plot([freqs[i][j] for i in range(0,N)],c=fc)
            handles.append(mpatches.Patch(color=fc))
        labels = [chr(ord('A')+i) for i in range(0,num_opts)]
        ax.legend(handles=handles,labels=labels,loc='upper left')
        f.savefig("outputs/frequency_plot_N{0}_mu{1}_ns{2}_no{3}.png".format(N,mu,n_seeds,num_opts),dpi=400)
        print "Frequency figure saved. Animating"
        animate_attr_spread(data=data)

    elif args[0] == "many":
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


    elif args[0] =="fixation":
        print "nothing yet"
