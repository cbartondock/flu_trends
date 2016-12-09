from universal import *
from growth_simulator import *

def hamming_distance(adict1, adict2):
    hamming_distance=0
    joint_keys = list(set(adict1.keys()).union(set(adict2.keys())))
    for key in joint_keys:
        if not (key in adict1.keys() and key in adict2.keys() and adict1[key]==adict2[key]):
            hamming_distance+=1
    return hamming_distance/float(len(joint_keys))

def get_final_similarity(data, choice_f):
    final_r = int(round(np.sqrt(data["pop"]/np.pi)))
    scaled_attr = {(seed[0], seed[1]):seed[3] for seed in seed_disk(final_r, choice_f)}
    return hamming_distance(data["attr"], scaled_attr)

def get_similarity_function(data, choice_f):
    generations = [zip(*zip(*gen)[:2]) for gen in data["gens"]]
    adict = data["attr"]
    pop=data["pop"]
    print "#gens: " + str(len(generations))
    seeds = generations[0]
    similarity=[]
    actual_attr={}
    scaled_attr={}
    r_in=0
    r_out=0
    sim=0
    i=0
    while i <len(generations) and sim<.4:
        actual_attr.update({deme: adict[deme] for deme in generations[i]})
        r_out = int(np.round((pop[i]/np.pi)**.5))
        scaled_seeds = seed_annulus(r_in,r_out,choice_f)
        scaled_attr.update({(seed[0],seed[1]): seed[3] for seed in scaled_seeds})
        sim=hamming_distance(actual_attr,scaled_attr)
        similarity.append(sim)
        r_in=r_out
        print "similarity["+str(i)+"]= "+str(similarity[i])
        i+=1
    return similarity



if __name__=="__main__":
    choice_f = bubble_choice_f(5)
    data=c_outbreak(2.0,10**5,seed_disk(10,choice_f))
    similarity = get_similarity_function(data, choice_f)





