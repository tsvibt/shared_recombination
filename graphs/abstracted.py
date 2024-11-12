from matplotlib import pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
from diskcache import Index

exec(open('stats.py').read())
exec(open('main.py').read())

plt.rcParams["figure.figsize"] = [18, 9]
plt.rcParams["figure.autolayout"] = True
fig, ax = plt.subplots()

segment_count = 100
sample_count = 3_0_000

Use_Cache = True
def GetData(segment_count, sample_count): 
   index = Index('./caches/') 
   key = (segment_count, sample_count)
   if Use_Cache and key in index: return index[key]
   else: 
      results = [Diploid(segment_count).datas() for _ in range(sample_count)]
      index[key] = results
      return results

print('getting data...')
datas = GetData(segment_count, sample_count) 
print('done getting data.')




def plot_finish(plot):
   plot.legend()
   plot.grid()

   import time
   filename = './images/' + globals().get('auxilliary_image_filename', 'graph') + str(round(time.time())) + '.png'
   plot.savefig(filename)
   plot.show()


BOOP

