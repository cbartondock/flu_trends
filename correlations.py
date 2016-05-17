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
    twopoint = Counter()
    for cone in cones:
        flat_cone = [deme for gen in cone for deme in gen]
        for i in range(0,len(flat_cone)):
            for j in range(0, i):
                if flat_cone[i][2] >= flat_cone[j][2]:
                    dx = flat_cone[i][0] - flat_cone[j][0]
                    dy = flat_cone[i][1] - flat_cone[j][1]
                    dt = flat_cone[i][2] - flat_cone[j][2]
                    if (dx**2+dy**2)**.5 < l(2*dt):
                        twopoint[(1./l(dt))*(dx**2+dy**2)**.5]+=1
    total = sum(twopoint.values())
    for key, value in twopoint.items():
        twopoint[key] = float(value) / total
    return twopoint



if __name__ == '__main__':
    cones = []
    n_cones = 15
    for i in range(0,n_cones):
        cones.append(simulate_outbreak(40,1.8)[1])
    twopoint = get_twopoint(cones, get_scaling(1.8))

