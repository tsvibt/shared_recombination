'''
exec(open('main.py').read())

exec(open('graphs/averages.py').read())
want to graph with x-axis is the SDs, and y-axis is probability, and the different curves are different selection procedures. 
'''

import numpy as np
import itertools

class Chromosome():
   def __init__(self, segment_count, total_variance):
      self.segment_count = segment_count
      self.total_variance = total_variance
      self.segment_variance = self.total_variance / self.segment_count
      self.segment_SD = np.sqrt(self.segment_variance)
      self.segments = np.random.normal(loc=0, scale=self.segment_SD, size=self.segment_count)
      self._cache_partial_sums = np.concatenate(([0], np.cumsum(self.segments)))
      self.partial_sum = (self._cache_partial_sums, self._cache_partial_sums[self.segment_count] - self._cache_partial_sums)

   def sum(self): return self.partial_sum[0][self.segment_count] 

class Diploid():
   def __init__(self, segment_count=10, total_variance = 1):
      self.segment_count = segment_count
      self.total_variance = total_variance
      self.total_SD_size = np.sqrt(self.total_variance)
      self.segment_variance = self.total_variance / self.segment_count
      self.segment_SD = np.sqrt(self.segment_variance)
      self.chromosomes = [Chromosome(segment_count, total_variance) for _ in [0,1]]
      self.recombinations = [sum(self.chromosomes[chr_num].partial_sum[i] for i, chr_num in enumerate([leader_chr, 1-leader_chr]))
            for leader_chr in [0,1]]
      self.max_recombinations = np.max(self.recombinations, 0)
      self.max_recombination = np.max(self.max_recombinations)
      self.max_chromosome = max(chr.sum() for chr in self.chromosomes)
      assert self.subdivisions_max_recombination(1)[1] == self.max_chromosome

      self.partial_sum_right_switchers = [self.chromosomes[chr_num].partial_sum[1] - self.chromosomes[1-chr_num].partial_sum[1]
                                          for chr_num in [0,1]]

      self.two_recombinations = np.full((2, self.segment_count, self.segment_count), -1000.0)
      for i,j in itertools.combinations_with_replacement(range(self.segment_count), 2):
         for chr_num in [0,1]:
            self.two_recombinations[chr_num][i][j] = self.recombinations[chr_num][i]+self.partial_sum_right_switchers[chr_num][j]
      self.max_two_recombinations = np.max(self.two_recombinations, 0)
      self.max_two_recombination = np.max(self.max_two_recombinations)

   def subdivisions_max_recombination(self, subdivisions):
      subdivision_length = self.segment_count // subdivisions
      cap = subdivision_length * subdivisions
      recombinations = self.max_recombinations[:cap:subdivision_length]
      return (len(recombinations), np.max(recombinations))

   def subdivisions_max_two_recombination(self, subdivisions):
      subdivision_length = self.segment_count // subdivisions
      cap = subdivision_length * subdivisions
      recombinations = self.max_two_recombinations[:cap:subdivision_length, :cap:subdivision_length]
      return (len(recombinations), np.max(recombinations))

   def datas(self):
      result = {
            'first chromosome': self.chromosomes[0].sum(),
            'best recombination': self.max_recombination,
            'best two recombination': self.max_two_recombination,
            'best chromosome': self.max_chromosome,
            } 
      scale = int(np.sqrt(self.segment_count))
      for subdivisions in list(range(2,scale)) + [self.segment_count // i for i in range(scale, 1, -1)]:
         actual_subdivisions, max_recomb = self.subdivisions_max_recombination(subdivisions)
         result[f'SUBDIVISIONS:{actual_subdivisions}'] = max_recomb

         actual_subdivisions, max_two_recomb = self.subdivisions_max_two_recombination(subdivisions)
         result[f'TWO_SUBDIVISIONS:{actual_subdivisions}'] = max_two_recomb
      return result 
   


