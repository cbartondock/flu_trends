from universal import *
from growth_simulator import *

def to_csv(infected, N, mu):
    with open("D3/outbreak_vis/data/inf_data_N{0}_mu{1}.csv".format(N,int(10*mu)), "wb") as f:
        writer = csv.writer(f)
        writer.writerow(['x','y','t'])
        writer.writerows(infected)

if __name__ == "__main__":
    N = 120
    mu = 3
    inf = c_outbreak(N, mu)["infected"]
    to_csv(inf, N, mu)
