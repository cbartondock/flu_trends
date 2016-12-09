from universal import *
from growth_simulator import *

def apply_me(args):
    print "applying"
    return c_outbreak(*args)

def many_sims(mus, mp,seeds,n_sim):
    def arg_gen():
        for i in range(0, n_sim):
            yield (mus[i%len(mus)],mp,seeds)
    pool = Pool(multiprocessing.cpu_count())
    return pool.map(apply_me, [args for args in arg_gen()])

if __name__ == "__main__":
    mus = [1.3,1.6, 1.9, 2.0, 2.3,2.6,2.9]
    mp = int(10**4)
    n_sim = 200
    n_attr= 2
    n_seeds = 1 if n_attr==1 else 20
    start = time.time()
    datadata = many_sims(mus,mp,seed_disk(30,choice_f=sector_choice_f([1,5])), n_sim)
    end = time.time()
    print "Elapsed Time: " + str(end-start)

    output_filename = "data_outputs/many_sims_t"+str(round(time.time()))+"+_mp{0}_nsim{1}_mus{2}_nattr{3}.pkl".format(mp,n_sim,"-".join([str(int(10*mu)) for mu in mus]),n_attr)
    data_output = open(output_filename, 'wb')
    pickle.dump(datadata,data_output)
    data_output.close()
