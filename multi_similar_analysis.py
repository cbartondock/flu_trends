from similarity_analysis import *
from multiple_sims import *
def geometric_dissipation(multiple_sims_data,choice_f):
    ts ={}
    counts={}
    devs={}
    out=[]
    for data in multiple_sims_data:
        mu=data["params"]["mu"]
        if mu not in out:
            if mu not in ts.keys():
                ts[mu]=0
                devs[mu]=0
                counts[mu]=0
            t=len(get_similarity_function(data,choice_f))
            if t>=len(data["gens"]):
                ts[mu]=0
                devs[mu]=0
                out.append(mu)
            ts[mu]+=t
            devs[mu]+=t**2
        counts[mu]+=1
    ts = {mu:t/float(counts[mu]) for mu, t in ts.items()}
    devs = {mu: (dev/float(counts[mu]) - ts[mu]**2)**.5 for mu,dev in devs.items()}
    return ts, devs

if __name__=="__main__":
    mus = [1+i/4. for i in range(0,8)]*10
    mp = 10**4
    n_sims=10
    multiple_sims_data = [c_outbreak(mu,mp,seed_disk(10,sector_choice_f([1,9]))) for mu in mus]#pickle.load(open("data_outputs/3.pkl",'r'))
    print "Done Opening"
    ts, devs = geometric_dissipation(multiple_sims_data,sector_choice_f([1,9]))
    seeds = multiple_sims_data[0]["gens"][0]
    adict = multiple_sims_data[0]["attr"]
    num_opts = len(list(set(adict.values())))
    colors = [(1.,1.,1.)]+[rc() for i in range(0,num_opts)]
    cmap1 = LinearSegmentedColormap.from_list("mycolors",colors)

    r = max([s[0] for s in seeds])
    dim = 1+2*r
    seed_matrix=[[0 for i in range(0,dim)] for j in range(0,dim)]
    for seed in seeds:
        seed_matrix[seed[1]+r][seed[0]+r] = adict[(seed[0],seed[1])]
    seedfig =plt.figure()
    seedax=seedfig.add_subplot(111)
    seedax.matshow(seed_matrix,vmin=0,vmax=num_opts,cmap=cmap1)
    seedax.axis('off')
    seedfig.savefig('temp.png')
    plt.clf()
    plt.close(seedfig)
    im = Image.open('temp.png')
    os.remove('temp.png')

    f = plt.figure()
    f.suptitle(r'Averaged $t_{mix}(\mu)$')
    ax=f.add_subplot(111)
    mt= zip(*[(mu,ts[mu]) for mu in ts.keys()])
    ax.scatter(mt[0],mt[1], color=rc(False))
    ax.errorbar(mt[0],mt[1],yerr=[devs[mu] for mu in mt[0]],color=rc(),fmt='o')
    ax.set_xlabel(r'$\mu$')
    ax.set_ylabel(r'$t_{mix}$')
    newax = f.add_axes([.2, 0.91, 0.08, 0.08], anchor='NE')
    newax.imshow(im,origin='lower')
    newax.set_ylabel('$t=0$')
    newax.tick_params(axis='both', left='off', top='off', right='off', bottom='off')
    newax.xaxis.set_major_formatter(plt.NullFormatter())
    newax.yaxis.set_major_formatter(plt.NullFormatter())

    f.savefig("outputs/average_mixing_time_plot_t"+str(round(time.time()))+"_mp{0}.png".format(tenexp(mp)),dpi=400)

