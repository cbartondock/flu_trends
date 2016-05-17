from universal import *
from scipy import integrate, interpolate

def analyze_kernel(filename):
    """Open the files produced by the growth simulation and use some version of the
    time reversal symmetry argument to extrapolate the jump kernel"""
    data_dump_file = open(filename,'rb')
    data_dump = pickle.load(data_dump_file)
    r_of_t = data_dump[2]
    (L, mu, N) = data_dump[4]
    kernel = invert_to_kernel_convolution(r_of_t)
    data_dump_file.close()
    kernel_output_filename = 'data_outputs/approx_kernel_data' + filename.split('simulation_data')[1]
    kernel_output = open(kernel_output_filename,'wb')
    pickle.dump([kernel,(L,mu,N)], kernel_output)
    kernel_output.close()
    return kernel_output_filename

def invert_to_kernel(r_of_t):
    print "Maximum Approx Method"
    t_of_r = {v: k for k, v in r_of_t.items()}
    kernel = [(l, -1 if t_of_r[l]*r_of_t[even_round(t_of_r[l]/2.)] == 0. or l<2 else 1./(t_of_r[l]*r_of_t[even_round(t_of_r[l]/2.)]**(2*d)))
            for l in r_of_t.values()]
    kernel = filter(lambda p: p[1]!=-1, kernel)
    return zip(*kernel)

def invert_to_kernel_convolution(r_of_t):
    print "Convolution Method"
    ts = r_of_t.keys()
    rs = r_of_t.values()
    kernel = []
    for T in range(1,len(ts)):
        integral = 0
        print "T = " + str(T)
        for t in range(0,T+1):
            print "t = " + str(t)
            integral += (r_of_t[t]*r_of_t[T-t])**(d)
        print integral
        kernel.append((r_of_t[T], -1 if integral == 0 or r_of_t[T] < 2 else 1/integral))
    kernel = filter(lambda p: p[1]!=-1, kernel)
    return zip(*kernel)

def invert_to_kernel_interp(r_of_t):
    print "Convolution Interpolation Method"
    ts = r_of_t.keys()
    rs = r_of_t.values()
    lp = interpolate.lagrange(ts, rs)
    kernel = []
    for T in range(1,len(ts)):
        lp2 = lambda t: (lp(t)*lp(T-t))**d
        integral = integrate.quad(lp2,0,T)[1]
        print integral
        kernel.append((r_of_t[T], -1 if integral == 0 or r_of_t[T] < 2 else 1/integral))
    kernel = filter(lambda p: p[1]!=-1, kernel)
    return zip(*kernel)

