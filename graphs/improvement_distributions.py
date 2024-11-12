
exec(open('graphs/abstracted.py').read())


Plot_distribution([data['best recombination'] - data['first chromosome'] for data in datas], 'best recombination - first', 'cyan')




