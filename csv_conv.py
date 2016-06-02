from universal import *
from growth_simulator import *

def to_csv(data, out):
    infected = data["infected"]
    attr_dict = data["attr"]
    access = lambda d: 0 if (d[0],d[1]) not in attr_dict else attr_dict[(d[0],d[1])]
    with open(out, "wb") as f:
        writer = csv.writer(f)
        writer.writerow(['x','y','t','k'])
        infected_with_attr = [(d[0],d[1],d[2], access(d)) for d in infected]
        writer.writerows(infected_with_attr)

if __name__ == "__main__":
    N = 150
    mu = 1.8
    num_seeds = 100
    choice_f = lambda d: choice([0,1,2,3,4,5])

    args = sys.argv[1:]
    if(len(args)==0 or args[0]=="spread"):
        inf_data = c_outbreak(N, mu)
        to_csv(inf_data,"d3/outbreak_vis/data/inf_data_N{0}_mu{1}.csv".format(N,int(10*mu)))
    elif(args[0]=="attr"):
        inf_data = c_outbreak(N, mu, seeds=seed_lattice(num_seeds), choice_f = choice_f)
        to_csv(inf_data,"d3/polya_vis/data/polya_data_N{0}_mu{1}.csv".format(N,int(10*mu)))
