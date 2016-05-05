def filter_cone(generations, seed, l):
    new_generations = [[seed]]+generations[seed[2]:]
    new_generations = [[deme in ng if distance(seed, deme) < l(deme[2]-seed[2])] for ng in new_generations
    return new_generations
