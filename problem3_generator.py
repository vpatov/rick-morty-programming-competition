# Cosmic readout generation

from random import randint, choice

f = open('cosmic_readouts.txt','w')

for num in range(1,51):

	width,height = randint(20,60),randint(20,60)
	dist_string = '#' + ('-' * randint(1,5))
	grid = '\n'.join([''.join([choice(dist_string) for i in range(width)]) for j in range(height)])
	print(width,height)
	print(grid)
	f.write(str(width) + ' ' + str(height) + '\n')
	f.write(grid + '\n')