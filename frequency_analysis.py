from universal import *
from growth_simulator import *

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
        for key, value in frequencies[i].items():
            frequencies[i][key]=value/float(totals[i])
    return frequencies


if __name__=="__main__":
    N=200
    mu=1.8
    n_seeds=50
    num_opts=2
    choice_f = even_choice_f(num_opts,n_seeds//num_opts)

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
"""
    fc = rc()
    fpatch = mpatches.Patch(color=fc)
    fitplot = radii_ax.plot([scaling(g) for g in range(0,N)],c=fc)
    radii_ax.set_xlabel(r'Generation')
    radii_ax.set_ylabel(r'Radius')
    radii_ax.legend(handles=[gyrplot,maxplot,fpatch],labels=[r'Gyration Radius', r'Maximum Radius', r'Crossover Prediction'], loc='upper left')
    radii_fig.savefig("outputs/radial_plot_N{0}_mu{1}.png".format(N,mu),dpi=400)
"""
