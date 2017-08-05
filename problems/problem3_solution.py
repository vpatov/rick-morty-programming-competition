grids = []
f = open('problem3_input.txt','r')
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

count_zpolsfhsdf = 0
get_neighbors = lambda x,y: ((x+1,y),(x,y+1),(x-1,y),(x,y-1))
def count_size_zone(grid,i,j,visited):
	cur = (i,j)
	if cur in visited:
		return 0
	else:
		if grid[i][j] == '#':
			visited.add(cur)
			neighbors = tuple(
				filter(
					lambda tup: 
						tup[0] < len(grid) and 
						tup[1] < len(grid[i]) and 
						tup[0] >= 0 and 
						tup[1] >= 0,
					get_neighbors(i,j)
					)
				)
			res = 0
			for x,y in neighbors:
				res += count_size_zone(grid,x,y,visited)
			return 1 + res
		else:
			return 0


def count_splin_zones(grid):
	visited = set()
	sizes = []
	for i in range(0,len(grid)):
		for j in range(0,len(grid[i])):
			cur = (i,j)
			if cur in visited or grid[i][j] != '#':
				continue
			else:
				sizes.append(count_size_zone(grid,i,j,visited))
	return (sorted(sizes)[::-1])


count = 0
for grid in grids:
	sizes = count_splin_zones(grid)
	if sizes[3] >= 5:
		count += 1
print(count)



def get_solution():
	return count
