import csv
import matplotlib.pylab as plt
from matplotlib.font_manager import FontProperties
from matplotlib import rc
from random import randrange

#Strictly Monotonic Bijection Dates <--> N
numify_year = lambda year: sum([a*int(b) for a,b in zip([365.25,29.53,1],year.split('-'))])
yearify_num = lambda num: '-'.join(map(lambda x: str(int(x)),[num/365.25,(num%365.25)/29.53,(num%365.25)%29.53]))
spaced_sample = lambda n, l: l[1::(len(l)//n)]

#Data Extraction
data=[]
filename = 'data_inputs/flu_data.csv'
with open(filename, 'rb') as csvfile:
    flu_reader = csv.reader(csvfile)
    for row in flu_reader:
        if len(row) > 5:
            data.append(row)
country_labels = data[0][1:]
data = data[1:]
print country_labels
data = zip(*data)
dates = map(numify_year, data[0])
data = data[1:]
data = [[0 if ili=='' else int(ili) for ili in row] for row in data]

#Probably Some Analysis
c = -2#randrange(0,len(country_labels))

#Plotting
plt.rc('text',usetex=True)
fig = plt.figure()
fig.suptitle(r'Influenza vs. Time for: {0}'.format(country_labels[c]),fontsize=14,fontweight='bold')
ax = fig.add_subplot(111)
fig.subplots_adjust(top=.85)
ax.plot(dates,data[c],'-', color='b',linewidth=.8)
plt.xticks(spaced_sample(4,dates),spaced_sample(4,map(yearify_num,dates)))
ax.tick_params(axis='x',pad=10)
ax.set_xlabel(r'\textsl{Year}')
ax.set_ylabel(r'\textsl{ILI Searches}')
ax.set_xlim([dates[0],dates[-1]])
ax.set_ylim([0,int(max(data[c])*1.2)])
plt.savefig('outputs/ILI_time_plot_of_{0}.pdf'.format(filename.split('.')[0]))
plt.clf()

