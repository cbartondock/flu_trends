from universal import *

def get_secondaries(gens):
    secondary_nodes = {}
    print len(gens)
    for g in range(0, len(gens)-1):
        print g
        xav = mean(map(lambda gen: mean(map(lambda p: p[0], gen)), gens[:g]))
        yav = mean(map(lambda gen: mean(map(lambda p: p[1], gen)), gens[:g]))
        metric = 1.2*mean_rad(xav,yav, gens[g])

        for deme in gens[g+1]:
            r_deme = distance(deme, (xav,yav))
            if r_deme > metric+1:
                source = True
                for s_node, s_node_info in secondary_nodes.items():
                    if distance(deme,s_node) < s_node_info[0]:
                        source = False
                        break
                if source:
                    node_info = (.14*(r_deme-metric), g+1)
                    secondary_nodes[deme] = node_info
    #sec_nodes is of the form source_node: (effective radius, global gen)
    print "Converting Format of Secondaries"
    secondary_outbreaks = {}
    secondary_r_of_ts = {}
    for s_node in secondary_nodes.keys():
        secondary_outbreaks[s_node] = [(s_node[0],s_node[1],secondary_nodes[s_node][1],0)]
        secondary_r_of_ts[s_node] = {0: 0}
    #sec_outbreaks is of the form source_node: [(node, global gen, local gen)]
    #sec_r_of_ts is of the form source_node: {local gen: r(gen)}

    for s_node, s_node_info in secondary_nodes.items():
        for g in range(s_node_info[1]+1, len(gens)):
            filtered_gen = [deme for deme in gens[g] if distance(deme,s_node) < s_node_info[0]]
            for deme in filtered_gen:
                secondary_outbreaks[s_node].append((deme[0], deme[1], s_node_info[1], g-s_node_info[1]))

            s_xav = mean(map(lambda p: p[0], secondary_outbreaks[s_node]))
            s_yav = mean(map(lambda p: p[1], secondary_outbreaks[s_node]))
            secondary_r_of_ts[s_node][g-s_node_info[1]] = gyr_rad(s_xav,s_yav, secondary_outbreaks[s_node])

#filter out the micro outbreaks
    secondary_outbreaks = {k: v for k, v in secondary_outbreaks.items() if len(v)>5 }
    secondary_r_of_ts = {k: v for k, v in secondary_r_of_ts.items() if len(secondary_outbreaks[k]) > 5 }

    return secondary_outbreaks, secondary_r_of_ts

def get_secondary_generational_r_of_t(secondary_outbreaks):
    r_of_t_secondary = []
    for source, outbreak in secondary_outbreaks.items():
        for i in range(0, len(outbreak)):
            distance_to_source = distance(outbreak[i],source)
            r_of_t_secondary.append( (outbreak[i][3], distance_to_source) )
    return r_of_t_secondary

def split_analyze(filename):
    data_dump_file = open(filename, 'rb')
    data_dump = pickle.load(data_dump_file)
    generations = data_dump[1]
    return get_secondaries(generations)[0]

def growth_rate_plot(secondary_outbreaks, filename):
    data_dump_file = open(filename, 'rb')
    data_dump = pickle.load(data_dump_file)
    generations = data_dump[1]
    (L, mu, N, d) = data_dump[4]

    l_of_t_primary = []
    for g in range(1, len(generations)-1):
        for deme in generations[g]:
            l_of_t_primary.append( (g, distance(deme, origin)) )
    l_of_t_secondary = get_secondary_generational_r_of_t(secondary_outbreaks)
    l_of_t_av_primary = time_average(l_of_t_primary)
    l_of_t_av_secondary = time_average(l_of_t_secondary)

    rfig = plt.figure()
    rfig.suptitle(r'$l(t)$ distribution with secondary outbreaks captured, $\mu={0}$'.format(mu),fontsize=14,fontweight='bold')
    r_ax = rfig.add_subplot(111)
    rfig.subplots_adjust(top=.9)
    primary_plot = r_ax.scatter(*zip(*l_of_t_primary), c='yellow', alpha=0.5)
    secondary_plot = r_ax.scatter(*zip(*l_of_t_secondary), c='red', alpha=0.5)
    plt.legend((primary_plot, secondary_plot), (r'$l(t)$ over primary outbreak', r'$l(t)$ over secondary outbreaks'),loc='upper left', ncol=1, fontsize=8)
    r_ax.set_xlabel(r'$t$')
    r_ax.set_ylabel(r'$l(t)$')
    rfig.savefig("outputs/suboutbreaks_growth_mu{0}_N{1}.png".format(mu,N),dpi=400)
    plt.clf()
    rav_fig = plt.figure()
    rav_fig.suptitle(r'$l(t)$ expectation with secondary outbreaks captured, $\mu={0}$'.format(mu),fontsize=14,fontweight='bold')
    rav_ax = rav_fig.add_subplot(111)
    rav_fig.subplots_adjust(top=.9)
    primary_average_plot = rav_ax.scatter(*zip(*l_of_t_av_primary), c='yellow', alpha=0.5)
    secondary_average_plot = rav_ax.scatter(*zip(*l_of_t_av_secondary), c='red',alpha=0.5)
    plt.legend((primary_average_plot, secondary_average_plot), (r'$E[l(t)]$ over primary outbreak', r'$E[l(t)]$ over secondary outbreaks'),loc='upper left', ncol=1, fontsize=8)
    rav_ax.set_xlabel(r'$t$')
    rav_ax.set_ylabel(r'$E[l(t)]$')
    rav_fig.savefig("outputs/suboutbreaks_average_growth_mu{0}_N{1}.png".format(mu,N),dpi=400)
    plt.clf()

def animate_secondary_outbreaks(secondary_outbreaks, filename):
    data_dump_file = open(filename, 'rb')
    data_dump = pickle.load(data_dump_file)
    generations = data_dump[1]
    all_demes = data_dump[0]
    (L, mu, N, d) = data_dump[4]
    infected_demes = []

    cm = plt.cm.get_cmap('hsv')
    animation_figure = plt.figure()
    animation_figure.suptitle(r'Secondary Outbreaks Plot with {0} generations, $\mu={1}$'.format(N,mu), fontsize = 14, fontweight='bold')
    ax = animation_figure.add_subplot(111)
    animation_figure.subplots_adjust(top=.9)
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Chris Dock'), bitrate=1800)

    colordict = {}
    for deme in all_demes:
        colordict[(deme[0], deme[1])] = 0
    s_outbreak_list = list(secondary_outbreaks.values())
    s_outbreak_list.reverse()
    for outbreak in s_outbreak_list:
        for outbreak_deme in outbreak:
            colordict[(outbreak_deme[0],outbreak_deme[1])] = outbreak[0][2];
    ims = []
    for i in range(1,len(generations)):
        print "i = " + str(i)
        for j in range(0, len(generations[i])):
            generations[i][j] = list(generations[i][j])
            generations[i][j][2] = colordict[(generations[i][j][0],generations[i][j][1])]
        infected_demes.extend(generations[i])
        xyt = zip(*infected_demes)
        ims.append((plt.scatter(xyt[0],xyt[1],c=xyt[2], norm = matplotlib.colors.Normalize(vmin=0,vmax=max(colordict.values())),cmap=cm, alpha=.8,marker='o',lw=0.0),))
    im_ani = animation.ArtistAnimation(animation_figure,ims,interval=50,repeat_delay=3000,blit=True)
    im_ani.save('outputs/split_outbreak_animation_N{0}_mu_{1}.mp4'.format(N,mu),writer=writer)


if __name__ == '__main__':
    args = sys.argv[1:]
    secondary_outbreaks =  split_analyze(args[0])

    growth_rate_plot(secondary_outbreaks, args[0])
    animate_secondary_outbreaks(secondary_outbreaks, args[0])
