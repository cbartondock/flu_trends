from universal import *
from kernel_analysis import *

def plot_spread(filename):
    data_dump_file = open(filename, 'rb')
    data_dump = pickle.load(data_dump_file)
    infected_demes = data_dump["infected"]
    (mu, N) = data_dump["params"]
    print "Plotting Spread"
    xyt = zip(*infected_demes)
    fig = plt.figure()
    fig.suptitle(r'Dispersal Plot with {0} generations, $\mu={1}$'.format(N,mu),fontsize=14,  fontweight='bold')
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=.9)
    cm = plt.cm.get_cmap('viridis')
    sc = ax.scatter(xyt[0],xyt[1],c=xyt[2],cmap=cm, alpha=.5,marker='o',lw=0.0)
    cbar = plt.colorbar(sc)
    cbar.solids.set_rasterized(True)
    cbar.solids.set_edgecolor("face")
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    fig.savefig("outputs/spread_plot_N{0}_mu{1}.png".format(N,mu), dpi=400)

def plot_radii(filename):
    data_dump_file = open(filename, 'rb')
    data_dump = pickle.load(data_dump_file)
    generations = data_dump["gens"]
    gyr_r_of_t = data_dump["gyr_r"]
    max_r_of_t = data_dump["max_r"]
    (mu, N) = data_dump["params"]
    scaling = get_crossover_scaling(mu)
    print "Plotting Radii"
    radii_fig = plt.figure()
    radii_fig.suptitle(r'Radial growth over {0} generations, $\mu={1}$'.format(N, mu),  fontweight='bold')
    radii_ax = radii_fig.add_subplot(111)
    radii_fig.subplots_adjust(top=.9)
    gyrplot = radii_ax.scatter(list(range(0,N)),[gyr_r_of_t[g] for g in range(0,N)], color=rc())
    maxplot = radii_ax.scatter(list(range(0,N)),[max_r_of_t[g] for g in range(0,N)], color=rc())
    fc = rc()
    fpatch = mpatches.Patch(color=fc)
    fitplot = radii_ax.plot([scaling(g) for g in range(0,N)],c=fc)
    radii_ax.set_xlabel(r'Generation')
    radii_ax.set_ylabel(r'Radius')
    radii_ax.legend(handles=[gyrplot,maxplot,fpatch],labels=[r'Gyration Radius', r'Maximum Radius', r'Crossover Prediction'], loc='upper left')
    radii_fig.savefig("outputs/radial_plot_N{0}_mu{1}.png".format(N,mu),dpi=400)

def plot_populations(filename):
    data_dump_file = open(filename,'rb')
    data_dump = pickle.load(data_dump_file)
    generations = data_dump["gens"]
    pop_of_t = data_dump["pop"]
    (mu, N) = data_dump["params"]
    print "Plotting Populations"
    pop_fig = plt.figure()
    pop_fig.suptitle(r'Population Plot with {0} generations, $\mu={1}$'.format(N,mu),fontsize=14,fontweight='bold')
    pop_ax = pop_fig.add_subplot(111)
    pop_fig.subplots_adjust(top=.9)
    pop_ax.plot([pop_of_t[g] for g in range(0,len(generations))])
    pop_ax.set_xlabel(r'Generation')
    pop_ax.set_ylabel(r'Total Population')
    pop_fig.savefig("outputs/population_plot_N{0}_mu{1}.png".format(N,mu),dpi=400)

def plot_kernel(kernel_filename):
    kernel_file = open(kernel_filename,'rb')
    kernel_data = pickle.load(kernel_file)
    kernel = kernel_data["kernel"]
    (mu, N) = kernel_data["params"]
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
    kernel_fig.savefig("outputs/kernel_plot_N{0}_mu{1}.png".format(N,mu), dpi=400)

def animate_spread(filename):
    data_dump_file = open(filename, 'rb')
    data_dump = pickle.load(data_dump_file)
    print data_dump
    generations = data_dump["gens"]
    (mu, N) = data_dump["params"]
    infected_demes = []
    cm = plt.cm.get_cmap('viridis')
    animation_figure = plt.figure()
    animation_figure.suptitle(r'Dispersal Plot with {0} generations, $\mu={1}$'.format(N,mu),fontsize=14,  fontweight='bold')
    ax = animation_figure.add_subplot(111)
    animation_figure.subplots_adjust(top=.9)
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Chris Dock'), bitrate=1800)

    ims = []
    for i in range(1,len(generations)):
        print "i = "+str(i)
        infected_demes.extend(generations[i])
        xyt = zip(*infected_demes)
        if xyt!=[]:
            ims.append((plt.scatter(xyt[0],xyt[1],c=xyt[2],cmap=cm, alpha=.5,marker='o',lw=0.0),))
    im_ani = animation.ArtistAnimation(animation_figure,ims,interval=50,repeat_delay=3000,blit=True)
    im_ani.save('outputs/spread_animation_N{0}_mu_{1}.mp4'.format(N,mu),writer=writer)



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
