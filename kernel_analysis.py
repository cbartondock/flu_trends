from universal import *
from scipy import integrate, interpolate
from plfit import plfit

def analyze_kernel(filename):
    """Open the files produced by the growth simulation and use some version of the
    time reversal symmetry argument to extrapolate the jump kernel"""
    outbreak_data_file = open(filename,'rb')
    print filename
    outbreak_data = pickle.load(outbreak_data_file)
    r_of_t = outbreak_data["mean_r"]
    mu = outbreak_data["params"]["mu"]
    mp = outbreak_data["params"]["mp"]
    kernel = invert_to_kernel_convolution(r_of_t)
    outbreak_data_file.close()
    kernel_output_filename = 'data_outputs/kernels/approx_kernel_data_mp{0}_mu{1}.pkl'.format(tenexp(mp),mu)
    kernel_output = open(kernel_output_filename,'wb')
    result = {"kernel": kernel, "params": {"mu":mu, "mp":mp}}
    pickle.dump(result, kernel_output)
    kernel_output.close()
    return kernel_output_filename

def invert_to_kernel(r_of_t):
    t_of_r = {v: k for k, v in r_of_t.items()}
    kernel = [(l, -1 if t_of_r[l]*r_of_t[even_round(t_of_r[l]/2.)] == 0. or l<2 else 1./(t_of_r[l]*r_of_t[even_round(t_of_r[l]/2.)]**(2*d)))
            for l in r_of_t.values()]
    kernel = filter(lambda p: p[1]!=-1, kernel)
    return zip(*kernel)

def invert_to_kernel_convolution(r_of_t):
    ts = r_of_t.keys()
    rs = r_of_t.values()
    kernel = []
    for T in range(1,len(ts)):
        integral = 0
        for t in range(0,T+1):
            integral += (r_of_t[t]*r_of_t[T-t])**(d)
        kernel.append((r_of_t[T], -1 if integral == 0 or r_of_t[T] < 1 else 1/integral))
    kernel = filter(lambda p: p[1]!=-1, kernel)
    return zip(*kernel)

#Unclear if Least Squares is the best approach here
def mu_retrieval(kernel):
    ls = np.asarray(kernel[0], dtype = 'float')
    gs = np.asarray(kernel[1], dtype = 'float')
    log_ls = np.log(ls)
    log_gs = np.log(gs)
    coefficients = np.polyfit(log_ls,log_gs,1)
    mu_approx = -(coefficients[0]+d)
    return mu_approx, coefficients, log_ls, log_gs, ls, gs
