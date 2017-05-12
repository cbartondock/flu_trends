from numpy.random import choice as choi
from numpy import pi
from numpy import log
from universal import *
lfunc = lambda t: 2**((log(t)**2)/8.)
tfunc = lambda l: np.e**(np.sqrt(8*log(l)/log(2)))
def fake_freq_sim(power,f0=[(1,100), (2,100)]):
    t0=1
    fs={t0:f0}
    freqs = {t0:{k:v for k,v in f0}}
    for i in range(1,power):
        t=2**i;
        npick = int(lfunc(t)/lfunc(t/2.))+1
        p = [fs[t/2][i][1] for i in range(len(fs[t/2]))]
        p = [entry/float(sum(p)) for entry in p]
        indices = list(choi(range(0,len(fs[t/2])),npick,p=p))
        new_f = [fs[t/2][i] for i in indices]
        new_f = [(typ,pi*lfunc(2*tfunc((A/pi)**.5))**2) for typ,A in new_f]
        new_freq = {j: 0 for j in list(set(zip(*f0)[0]))}
        for entry in new_f:
            new_freq[entry[0]]+=entry[1]
        new_freq = {k:v/sum(new_freq.values()) for k,v in new_freq.items()}
        freqs[t] = new_freq
        fs[t]=[(k,100*v) for k,v in new_freq.items()]
    return freqs

if __name__ == "__main__":
    n=10000
    power=20
    av_max_freqs={2**i:0 for i in range(0,power)}
    dev_max_freqs={2**i:0 for i in range(0,power)}
    for i in range(0,n):
        freqs = fake_freq_sim(power)
        maxfreqs = {t: max(freqs[t].values()) for t in freqs.keys()}
        for t in maxfreqs.keys():
            av_max_freqs[t]+=maxfreqs[t]
            dev_max_freqs[t]+=maxfreqs[t]**2
    av_max_freqs= {t:mf/float(n) for t,mf in av_max_freqs.items()}
    dev_max_freqs = {t: (d/float(n)-av_max_freqs[t]**2)**.5 for t, d in dev_max_freqs.items()}
    f = plt.figure()
    f.suptitle(r'Deviation in Largest Frequency vs. $t$',fontsize=14,fontweight='bold')
    ax= f.add_subplot(111)
    td = zip(*[(k,v) for k,v in dev_max_freqs.items()])
    ax.scatter(td[0],td[1],color=rc())
    ax.set_xlabel(r't')
    ax.set_xscale('log')
    ax.set_ylabel(r'$V[f_{max}]$')
    f.savefig("outputs/fakefreqplot_n{0}_power{1}_t".format(n,power)+str(round(time.time()))+".png",dpi=400)
