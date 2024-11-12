'''
exec(open('graphs/averages.py').read())
'''

exec(open('graphs/abstracted.py').read())

subdivision_average = []
subdivision_two_average = []

for datafield in datas[0].keys():
   if datafield.startswith('SUBDIVISIONS:'):
      subdivision_average.append((int(datafield.split(':')[1]) , np.average([data[datafield] for data in datas]) ))
   if datafield.startswith('TWO_SUBDIVISIONS:'):
      subdivision_two_average.append((int(datafield.split(':')[1]) , np.average([data[datafield] for data in datas]) ))

def things_plot(thingies, color, specials, crossover_num, label=None):
   global x_axis
   for subdivision_count, datafield in specials.items():
      thingies.append((subdivision_count, np.average([data[specials[subdivision_count]] for data in datas])))
   thingies = sorted(thingies)
   x_axis = [x[0] for x in thingies]
   y_axis = [x[1] for x in thingies]
   ax.plot(x_axis, y_axis,linestyle='dotted', color=color, label=(label or f'average SDs with {crossover_num} crossover points'))
   ax.scatter(x_axis, y_axis, color=color, s=223, alpha=.58, edgecolor='none')

   colors = ['orange', 'red', 'purple']
   color_index = 0
   for subdivision_count, average in thingies:
      if subdivision_count in [0,1,60]:
         if subdivision_count in specials:
            ax.scatter([subdivision_count], [average], color=colors[color_index], s=223, alpha=1, edgecolor='none', label=specials[subdivision_count])
            color_index += 1
            annotation = specials[subdivision_count]
         else: annotation = ''
      else:
         annotation = f'{subdivision_count}'
      ax.annotate(annotation, (subdivision_count+.01, average-.040))

special_points = {0: 'first chromosome', 1: 'best chromosome', 60: 'best recombination'}
things_plot(subdivision_average, 'green', special_points, 1)
special_two_points = {0: 'first chromosome', 1: 'best chromosome', 60: 'best two recombination'}
things_plot(subdivision_two_average, 'red', special_two_points, 2)

special_max = {}
things_plot([(i, i*gaussian_max_numerical(2, 1/np.sqrt(i), 0)) for i in x_axis if 0<i<21] , 'pink', special_max, 2, label = 'computed expectation of best chromosome, k divisions')


plt.ylabel("average SDs (the whole chromosome is standard gaussian)")
plt.xlabel(f"""number N of segments demarcated by N+1 allowed crossover points (equally spaced)
subdivisions of chromosomes: {segment_count}. samples: {sample_count:,}.
we sample {sample_count:,} diploid pairs of chromosomes, where each chromosome is a string of {segment_count} samples from gaussians, such that a chromosome is gaussian, mean=0, SD=1.
this graph shows the average over the population of the best recombination produced from the two chromosomes, where there are allowed to be crossover points at k/N for k in [0,N]""")

auxilliary_image_filename = 'Averages'
plt.gca().set_ylim(bottom=-.06)
plot_finish(plt)


