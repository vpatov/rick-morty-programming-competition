grids = []
with open('input_7.txt','r') as f:
	while(True):
		grid = []
		line = f.readline()
		if (len(line) < 1):
			break
		width,height = (int(i) for i in line.split())
		for row in range(height):
			line = f.readline().strip()
			grid.append(list(line))
		grids.append(grid)

print(grids)

