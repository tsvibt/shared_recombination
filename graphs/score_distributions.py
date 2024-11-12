'''
exec(open('graphs/score_distributions.py').read())
scalene graphs.py
'''

exec(open('graphs/abstracted.py').read())


SD_max = 4
SD_min = -2 
SD_range = SD_max - SD_min
assert SD_range % 2 == 0
subdivisions = 8
assert subdivisions % 2 == 0
divisions = SD_range*subdivisions+1

colors = ['orange', 'red', 'purple', 'green', 'black', ]

def Plot_distribution(datavalues, label, color):
   global x_axis
   counts, bin_edges = np.histogram(datavalues, bins=divisions, range=(SD_min, SD_max), density=True)
   bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
   x_axis = bin_centers
   ax.plot(x_axis, counts, linestyle='solid', color=color, label=label)
   avg = np.average(datavalues)
   ax.scatter([avg], [0], color=color, s=83, alpha=.48, edgecolor='none')#, label=datafield+' average')
   ax.vlines([avg], 0, counts[np.abs(x_axis - avg).argmin()], colors=color, linestyles='dotted', alpha=0.5)



print('making datafield graphs...')
subdivision_counts = [2,3,5,7,10,30,50]
for i,datafield in enumerate(datas[0].keys()):
   if (datafield.startswith('SUBDIVISIONS:') or datafield.startswith('TWO_SUBDIVISIONS:')) and int(datafield.split(':')[1]) not in subdivision_counts: continue
   Plot_distribution([data[datafield] for data in datas], datafield, colors[i%len(colors)])
print('done making datafield graphs.')


print('making extra graphs...')

ax.plot(x_axis, [standard_gaussian_pdf(x) for x in x_axis],linestyle='dashed', color='green', label='standard Gaussian')

ax.plot(x_axis, [gaussian_max_pdf(2, 1, 0, x) for x in x_axis],linestyle='dashed', color='blue', label='max 2 Gaussian')

j= list(x_axis[:len(x_axis)//2] - SD_range//2)
j.extend(x_axis)
j.extend(list(x_axis[(len(x_axis)//2)+1:] + SD_range//2))

g=np.array([gaussian_max_pdf(2, 1/np.sqrt(2), 0, x) for x in j])
gg= np.convolve(g,g)

SD_middle = SD_min + (SD_range // 2)
middle = (len(gg)//2) - (SD_middle*subdivisions) 

z=middle - (len(x_axis)//2)
zz=middle + (1+len(x_axis)//2)
ggg = gg[z:zz]*(x_axis[1]-x_axis[0])

ax.plot(x_axis, ggg, linestyle='dashed', color='pink', label='max 2 Gaussian, 2 segments')

print('done making extra graphs.')

plt.ylabel("probability density")
plt.xlabel(f"SDs\nsubdivisions of chromosomes: {segment_count}. samples: {sample_count:,}.")

plt.gca().set_ylim(bottom=-.01)
plot_finish(plt)


