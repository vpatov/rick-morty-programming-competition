# Cosmic readout generation

import random


grid = '\n'.join([''.join([random.choice('#---') for i in range(10)]) for j in range(10)])
print(grid)