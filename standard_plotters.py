from universal import *
from kernel_analysis import *
from frequency_analysis import *
from similarity_analysis import *

def plot_spread(filename,tstring):
    data_dump_file = open(filename, 'rb')
    data_dump = pickle.load(data_dump_file)
    infected_demes = data_dump["infected"]
    mu, mp = data_dump["params"]["mu"], data_dump["params"]["mp"]
    print "Plotting Spread"
    xyt = zip(*infected_demes)
    fig = plt.figure()
    fig.suptitle(r'Dispersal Plot with final pop. $10^{0}$, $\mu={1}$'.format(tenexp(mp), mu),fontsize=14,  fontweight='bold')
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=.9)
    cm = plt.cm.get_cmap('viridis')
    sc = ax.scatter(xyt[0],xyt[1],c=xyt[2],cmap=cm, alpha=.5,marker='o',lw=0.0)
    cbar = plt.colorbar(sc)
    cbar.solids.set_rasterized(True)
    cbar.solids.set_edgecolor("face")
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    newdir = "outputs/_t"+tstring+"_mp{0}_mu{1}".format(tenexp(mp),mu)
    if not os.path.isdir(newdir):
        os.mkdir(newdir)
    fig.savefig(newdir+"/spread_plot_t"+str(round(time.time()))+"_mp{0}_mu{1}.png".format(tenexp(mp),mu), dpi=400)
    plt.clf()
    plt.close(fig)

def plot_attr_spread(filename,tstring):
    data_dump_file = open(filename, 'rb')
    data_dump = pickle.load(data_dump_file)
    infected_demes = data_dump["infected"]
    mu, mp = data_dump["params"]["mu"], data_dump["params"]["mp"]
    attr_dict = data_dump["attr"]
    print "Plotting Attribute Spread"
    xyt = zip(*infected_demes)
    fig = plt.figure()
    fig.suptitle(r'Dispersal Plot with final pop. $10^{0}$, $\mu={1}$'.format(tenexp(mp),mu),fontsize=14,  fontweight='bold')
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=.9)
    cs = [attr_dict[(xyt[0][i],xyt[1][i])]/float(5) for i in range(0,len(xyt[0]))]
    cm = plt.cm.get_cmap('hsv')
    sc = ax.scatter(xyt[0],xyt[1],c=cs,vmin=0.,vmax=1.,cmap=cm,alpha=.5,marker='o',lw=0.0)
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    newdir = "outputs/_t"+tstring+"_mp{0}_mu{1}".format(tenexp(mp),mu)
    if not os.path.isdir(newdir):
        os.mkdir(newdir)

    fig.savefig(newdir+"/attr_plot_t"+str(round(time.time()))+"_mp{0}_mu{1}.png".format(tenexp(mp),mu), dpi=400)
    plt.clf()
    plt.close(fig)

def plot_radii(filename, tstring):
    data_dump_file = open(filename, 'rb')
    data_dump = pickle.load(data_dump_file)
    generations = data_dump["gens"]
    mean_r_of_t = data_dump["mean_r"]
    max_r_of_t = data_dump["max_r"]
    mu, mp = data_dump["params"]["mu"], data_dump["params"]["mp"]
    asym_scaling = get_asymptotic_scaling(mu)

    crit_scaling = get_critical_scaling()
    print "Plotting Radii"
    radii_fig = plt.figure()
    radii_fig.suptitle(r'Radial growth with final pop. $10^{0}$, $\mu={1}$'.format(tenexp(mp), mu),  fontweight='bold')
    radii_ax = radii_fig.add_subplot(111)
    radii_fig.subplots_adjust(top=.9)
    gs = range(0,len(generations))
    mean_rs = [mean_r_of_t[g] for g in gs]
    max_rs = [max_r_of_t[g] for g in gs]
    meanplot = radii_ax.scatter(list(gs), mean_rs, color=rc())

    fc, fc2 = rc(),rc()
    fpatch, fpatch2 = mpatches.Patch(color=fc), mpatches.Patch(color=fc2)
    fitfunc = lambda scaling: np.vectorize(lambda t, *p: p[0]*(scaling(t)-scaling(0)))
    #p_asym, cov_asym = curve_fit(fitfunc(asym_scaling), gs[:10], mean_rs[:10], p0=(1,))
    p_crit, cov_crit = curve_fit(fitfunc(crit_scaling), np.asarray(gs), np.asarray(mean_rs),p0=(1,))
    critplot = radii_ax.plot([fitfunc(crit_scaling)(g, *p_crit) for g in gs],c=fc2)
    #asymplot = radii_ax.plot([fitfunc(asym_scaling)(g, *p_crit) for g in gs],c=fc)
    radii_ax.set_xlabel(r'Generation')
    radii_ax.set_ylabel(r'Radius')
    radii_ax.legend(handles=[meanplot,fpatch2],labels=[r'Mean Radius', r'Critical Prediction'], loc='upper left')
    newdir = "outputs/_t"+tstring+"_mp{0}_mu{1}".format(tenexp(mp),mu)
    if not os.path.isdir(newdir):
        os.mkdir(newdir)
    radii_fig.savefig(newdir+"/radial_plot_t"+str(round(time.time()))+"_mp{0}_mu{1}.png".format(tenexp(mp),mu),dpi=400)
    maxplot = radii_ax.scatter(list(gs),max_rs, color=rc())
    radii_ax.legend(handles=[meanplot,maxplot,fpatch2],labels=[r'Mean Radius', r'Maximum Radius', r'Critical Prediction'], loc='upper left')
    radii_fig.savefig(newdir+"/max_radial_plot_t"+str(round(time.time()))+"_mp{0}_mu{1}.png".format(tenexp(mp),mu),dpi=400)
    plt.clf()
    plt.close(radii_fig)

def plot_populations(filename,tstring):
    data_dump_file = open(filename,'rb')
    data_dump = pickle.load(data_dump_file)
    generations = data_dump["gens"]
    pop_of_t = data_dump["pop"]
    mu, mp = data_dump["params"]["mu"], data_dump["params"]["mp"]
    print "Plotting Populations"
    pop_fig = plt.figure()
    pop_fig.suptitle(r'Population Plot with final pop. $10^{0}$, $\mu={1}$'.format(tenexp(mp),mu),fontsize=14,fontweight='bold')
    pop_ax = pop_fig.add_subplot(111)
    pop_fig.subplots_adjust(top=.9)
    pop_ax.plot([pop_of_t[g] for g in range(0,len(generations))])
    pop_ax.set_xlabel(r'Generation')
    pop_ax.set_ylabel(r'Total Population')
    newdir = "outputs/_t"+tstring+"_mp{0}_mu{1}".format(tenexp(mp),mu)
    if not os.path.isdir(newdir):
        os.mkdir(newdir)
    pop_fig.savefig(newdir+"/population_plot_t"+str(round(time.time()))+"_mp{0}_mu{1}.png".format(tenexp(mp),mu),dpi=400)
    plt.clf()
    plt.close(pop_fig)

def plot_frequencies(filename, tstring, data=[]):
    print "Plotting Frequency"
    if data==[]:
        data_dump_file = open(filename, 'rb')
        data_dump = pickle.load(data_dump_file)
        data_dump_file.close()
    else:
        data_dump = data
    mu, mp = data_dump["params"]["mu"], data_dump["params"]["mp"]
    freqs = get_frequency_functions(data_dump)
    num_opts = len(list(set(freqs[0].values())))
    seeds = data_dump["gens"][0]
    adict = data_dump["attr"]
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
    f.suptitle(r'$f(t)$ with final pop. $10^{0}$, $\mu={1}$'.format(tenexp(mp),mu),fontsize=14,fontweight='bold')
    ax = f.add_subplot(111)
    ax.set_xlabel(r'Generation');
    ax.set_ylabel(r'$f$')
    handles=[]
    for j in range(1, num_opts+1):
        fc=rc()
        ax.plot([freqs[i][j] for i in range(0,len(freqs))],c=colors[j])
        handles.append(mpatches.Patch(color=colors[j]))
    labels = [chr(ord('A')+i) for i in range(0,num_opts)]
    ax.legend(handles=handles,labels=labels,loc='upper left')
    newax = f.add_axes([.2, 0.91, 0.08, 0.08], anchor='NE')
    newax.imshow(im,origin='lower')
    newax.set_ylabel('$t=0$')
    newax.tick_params(axis='both', left='off', top='off', right='off', bottom='off')
    newax.xaxis.set_major_formatter(plt.NullFormatter())
    newax.yaxis.set_major_formatter(plt.NullFormatter())
    newdir = "outputs/_t"+tstring+"_mp{0}_mu{1}".format(tenexp(mp),mu)
    if not os.path.isdir(newdir):
        os.mkdir(newdir)
    f.savefig(newdir+"/frequency_plot_t"+str(round(time.time()))+"_mp{0}_mu{1}_no{2}.png".format(tenexp(mp),mu,num_opts),dpi=400)
    plt.clf()
    plt.close(f)

def plot_similarity(choice_f, filename, tstring, data=[]):
    print "Plotting Similarity"
    if data==[]:
        data_dump_file = open(filename, 'rb')
        data_dump = pickle.load(data_dump_file)
        data_dump_file.close()
    else:
        data_dump = data
    mu, mp = data_dump["params"]["mu"], data_dump["params"]["mp"]
    similarity = get_similarity_function(data_dump, choice_f)
    seeds = data_dump["gens"][0]
    adict = data_dump["attr"]
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
    f.suptitle(r'$\mu_H(t)$ with final pop. $10^{0}$, $\mu={1}$'.format(tenexp(mp),mu),fontsize=14,fontweight='bold')
    ax = f.add_subplot(111)
    ax.set_xlabel(r'Generation');
    ax.set_ylabel(r'Hamming Distance $\mu_H$')
    ax.plot(similarity, c =rc())
    newax = f.add_axes([.2, 0.91, 0.08, 0.08], anchor='NE')
    newax.imshow(im,origin='lower')
    newax.set_ylabel('$t=0$')
    newax.tick_params(axis='both', left='off', top='off', right='off', bottom='off')
    newax.xaxis.set_major_formatter(plt.NullFormatter())
    newax.yaxis.set_major_formatter(plt.NullFormatter())
    newdir = "outputs/_t"+tstring+"_mp{0}_mu{1}".format(tenexp(mp),mu)
    if not os.path.isdir(newdir):
        os.mkdir(newdir)
    f.savefig(newdir+"/similarity_plot_t"+str(round(time.time()))+"_mp{0}_mu{1}.png".format(tenexp(mp),mu),dpi=400)
    plt.clf()
    plt.close(f)

def animate_spread(filename,tstring):
    data_dump_file = open(filename, 'rb')
    data_dump = pickle.load(data_dump_file)
    data_dump_file.close()
    generations = data_dump["gens"]
    mu, mp = data_dump["params"]["mu"], data_dump["params"]["mp"]
    infected_demes = []
    cm = plt.cm.get_cmap('viridis')
    animation_figure = plt.figure()
    animation_figure.suptitle(r'Dispersal Plot with final pop. $10^{0}$, $\mu={1}$'.format(tenexp(mp),mu),fontsize=14,  fontweight='bold')
    ax = animation_figure.add_subplot(111)
    animation_figure.subplots_adjust(top=.9)
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=5, metadata=dict(artist='Chris Dock'), bitrate=2000)

    ims = []
    endmax = max_rad(0,0,generations[-1])
    for i in range(0,len(generations)):
        print "progress: "+str(float(i)/len(generations))
        infected_demes.extend(generations[i])
        xyt = zip(*infected_demes)
        if xyt!=[]:
            scaled_xs = [x*endmax/max_radii[i] for x in xyt[0]]
            scaled_ys = [y*endmax/max_radii[i] for y in xyt[1]]
            ims.append((plt.scatter(scaled_xs,c=xyt[2],cmap=cm,alpha=.9,marker='o',lw=0.0),))
    im_ani = animation.ArtistAnimation(animation_figure,ims,interval=50,blit=True)
    newdir = "outputs/_t"+tstring+"_mp{0}_mu{1}".format(tenexp(mp),mu)
    if not os.path.isdir(newdir):
        os.mkdir(newdir)
    im_ani.save(newdir+"/spread_animation_t"+str(round(time.time()))+"_mp{0}_mu_{1}.mp4".format(tenexp(mp),mu),writer=writer,dpi=500)
    plt.clf()
    plt.close()

def animate_attr_spread(filename,tstring, data=[]):
    if data==[]:
        data_dump_file = open(filename, 'rb')
        data_dump = pickle.load(data_dump_file)
        data_dump_file.close()
    else:
        data_dump=data
    generations = data_dump["gens"]
    attr_dict = data_dump["attr"]
    mu, mp = data_dump["params"]["mu"], data_dump["params"]["mp"]
    infected_demes = []
    cm = plt.cm.get_cmap('hsv')
    animation_figure = plt.figure()
    animation_figure.suptitle(r'Dispersal Plot with final pop. $10^{0}$, $\mu={1}$'.format(tenexp(mp),mu),fontsize=14,  fontweight='bold')
    ax = animation_figure.add_subplot(111)
    animation_figure.subplots_adjust(top=.9)
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=5, metadata=dict(artist='Chris Dock'), bitrate=2000)

    ims = []
    endrad = max_rad(0,0, generations[-1])
    rad = max_rad(0,0,generations[0])
    for i in range(0,len(generations)):
        print "progress: "+str(float(i)/len(generations))
        infected_demes.extend(generations[i])
        xyt = zip(*infected_demes)
        cs = [attr_dict[(xyt[0][j],xyt[1][j])] for j in range(0,len(xyt[0]))]
        if xyt!=[]:
            rad = max(rad,max_rad(0,0,generations[i]))
            scaled_xs = [x*endrad/rad for x in xyt[0]]
            scaled_ys = [y*endrad/rad for y in xyt[1]]
            ims.append((plt.scatter(scaled_xs,scaled_ys,c=cs,vmin=0.,vmax=max(attr_dict.values()),cmap=cm, alpha=.9,marker='o',lw=0.0),))
    im_ani = animation.ArtistAnimation(animation_figure,ims,interval=50,blit=True)
    newdir = "outputs/_t"+tstring+"_mp{0}_mu{1}".format(tenexp(mp),mu)
    if not os.path.isdir(newdir):
        os.mkdir(newdir)
    im_ani.save(newdir+"/attr_spread_animation_t"+str(round(time.time()))+"_mp{0}_mu_{1}.mp4".format(tenexp(mp),mu),writer=writer,dpi=500)
    plt.clf()
    plt.close()

def plot_kernel(kernel_filename,tstring):
    kernel_file = open(kernel_filename,'rb')
    kernel_data = pickle.load(kernel_file)
    kernel = kernel_data["kernel"]
    mu, mp = kernel_data["params"]["mu"], kernel_data["params"]["mp"]
    print "Plotting Kernel"
    kernel_fig = plt.figure()
    kernel_fig.suptitle(r'Approximated Jump Kernel for simulation, $\mu={0}$'.format(mu))
    kernel_ax = kernel_fig.add_subplot(111)
    kernel_fig.subplots_adjust(top=.9)
    kernel_ax.set_yscale('log')
    kernel_ax.set_xscale('log')
    kernel_ax.set_xlabel(r'$\log(l)$')
    kernel_ax.set_ylabel(r'$\approx \log(G(l))$')
    kernel_ax.plot(*kernel)

    ls = np.asarray(kernel[0], dtype = 'float')
    gs = np.asarray(kernel[1], dtype = 'float')
    log_ls = np.log(ls)
    log_gs = np.log(gs)
    coefficients = np.polyfit(log_ls,log_gs,1)
    print "Actual mu = " + str(mu)
    print "Slope Approximated mu = " + str(-(coefficients[0]+d))
    print coefficients[1]
    print "Intercept Approximated mu = " + str(np.exp(abs(coefficients[1])))
    print "Relative Slope error = " + str(abs(mu+coefficients[0]+d)/mu)
    polynomial = np.poly1d(coefficients)
    plt.text(0.4,.2,r'$\log{G(l)}\approx'+str(round(coefficients[0],2))+'\log(l)+'+str(round(coefficients[1],2))+'$', horizontalalignment='center',verticalalignment='center',transform=kernel_ax.transAxes)
    fit_log_gs = polynomial(log_ls)
    kernel_ax.plot(ls,np.exp(fit_log_gs))
    newdir = "outputs/_t"+tstring+"_mp{0}_mu{1}".format(tenexp(mp),mu)
    if not os.path.isdir(newdir):
        os.mkdir(newdir)
    kernel_fig.savefig(newdir+"/kernel_plot_t"+str(round(time.time()))+"_mp{0}_mu{1}.png".format(tenexp(mp),mu), dpi=400)
    plt.clf()
    plt.close(kernel_fig)



if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)!=2:
        print "Directly running plotters.py requires two arguments, the plotter name and the data file"
        print "Valid options for plotter name are spread, radii, pops, animate, kernel, or all"
        sys.exit()
    f = args[1]
    p = args[0]
    if p == 'spread' or p == 'all':
        plot_spread(f)
    if p == 'radii' or p == 'all':
        plot_radii(f)
    if p == 'pops' or p == 'all':
        plot_populations(f)
    if p == 'kernel':
        plot_kernel(f)
    if p == 'animate':
        animate_spread(f)
    if p == 'attr':
        plot_attr_spread(f)
    if p == 'animate_attr':
        animate_attr_spread(f)
