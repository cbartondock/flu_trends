from growth_simulator import simulate_outbreak
from universal import *

def get_sep_distr(cone):
    distances = []
    for gen in cone:
        for i in range(0,len(gen)):
            for j in range(0,i):
                d = ((gen[i][0]-gen[j][0])**2+(gen[i][1]-gen[j][1])**2)**.5
                distances.append(d)
    max_d = max(distances)
    min_d = min(distances)
    num_distances = len(distances)
    resolution = 1000.
    step = (max_d - min_d)/1000.
    sep_distr = Counter()
    for distance in distances:
        sep_distr[min_d +(.5 + (distance//step))*step] += 1
    sep_distr = dict(sep_distr)
    for key, value in sep_distr.items():
        sep_distr[key] = float(value) / num_distances
    return sep_distr

def get_twopoint(cones,l):
    correlator = Counter()

    for m in range(0,len(cones)):
        cone = cones[m]
        print m
        for g in range(1,len(cone)):
            cone[g].extend(map(lambda p: (p[0],p[1],g), cone[g-1]))
        flat_cone = [deme for gen in cone for deme in gen]

        for i in range(0,len(flat_cone)):
            for j in range(0, i+1):
                    x1 = flat_cone[i][0]
                    x2 = flat_cone[j][0]
                    y1 = flat_cone[i][1]
                    y2 = flat_cone[j][1]
                    t1 = flat_cone[i][2]
                    t2 = flat_cone[j][2]
                    correlator[(x1,x2,y1,y2,t1,t2)]+=1
    for key, value in correlator.items():
        correlator[key] = float(value) / len(cones)

    twopoint = Counter()
    for c, v in correlator.items():
        twopoint[(round(((c[0]-c[1])**2+(c[2]-c[3])**2)**.5,2),abs(c[4]-c[5]))]=v
    return twopoint



if __name__ == '__main__':
    cones = []
    n_cones = 100
    mu = 1.8
    for i in range(0,n_cones):
        cones.append(simulate_outbreak(20, mu)[1])
    twopoint = get_twopoint(cones, get_scaling(mu))

    print "Plotting"
    fig = plt.figure()
    fig.suptitle("Two Point Correlation Function for $\mu={0}$".format(mu),fontsize=14,fontweight='bold')
    ax = fig.add_subplot(111, projection = '3d')
    variables = zip(*twopoint.keys())
    ax.scatter(variables[0],variables[1],twopoint.values())
    ax.set_xlabel(r'$dr$')
    ax.set_ylabel(r'$dt$')
    ax.set_zlabel(r'$\varepsilon(dt, dr)$')
    fig.savefig("outputs/twopoint_mu{0}.png".format(mu),dpi=400)
    plt.show()
    plt.clf()

