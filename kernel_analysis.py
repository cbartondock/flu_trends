from universal import *


def analyze_kernel(filename):
    """Open the files produced by the growth simulation and use some version of the
    time reversal symmetry argument to extrapolate the jump kernel"""
    data_dump_file = open(filename,'rb')
    data_dump = pickle.load(data_dump_file)
    r_of_t = data_dump[2]
    (L, mu, N, d) = data_dump[4]
    kernel = invert_to_kernel(r_of_t, N)
    data_dump_file.close()
    kernel_output_filename = 'data_outputs/approx_kernel_data' + filename.split('simulation_data')[1]
    kernel_output = open(kernel_output_filename,'wb')
    pickle.dump([kernel,(L,mu,N,d)], kernel_output)
    kernel_output.close()
    return kernel_output_filename

def invert_to_kernel(r_of_t, N):
    #r_of_t = {k: v for k, v in r_of_t.items() if v!=0.}
    t_of_r = {v: k for k, v in r_of_t.items()}
    kernel = [(l, (-1 if t_of_r[l]*r_of_t[even_round(t_of_r[l]/2.)] == 0. or l<2 else 1./(t_of_r[l]*r_of_t[even_round(t_of_r[l]/2.)]**(2*d))))
            for l in r_of_t.values()]
    kernel = filter(lambda p: p[1]!=-1, kernel)
    kernel = zip(*kernel)
    return kernel
