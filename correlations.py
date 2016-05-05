from growth_simulator import simulate_outbreak
from universal import *

def get_distance_correlation_function(cone)
    demes = flatten(cone)
    distances = []
    for i in range(0,len(demes)):
        for j in range(0,i):
            d = distance(demes[i],demes[j])
            distances.append(d)
    max_d = max(distances)
    min_d = min(distances)
    num_distances = len(distances)
    resolution = 1000.
    step = (max_d - min_d)/1000.
    correlation_function = Counter()
    for distance in distances:
        correlation_function[min_d +(.5 + floor(distance/step))*step] += 1
    correlation_function = dict(correlation_function)
    for key, value in correlation_function.items():
        correlation_function[key] = float(value) / num_distances


if __name__ == '__main__':
    data_from_outbreak = simulate_outbreak(1,8, actual_mu, True, -1, 3)
    #print [(int(p[0]),p[1]) for g in data_from_outbreak for p in g]
    #l = scaling(data_from_outbreak, init_mu)
    all_cones_plot(data_from_outbreak)

