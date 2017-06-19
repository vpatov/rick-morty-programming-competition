import math
f = open('problem1_input.txt','r')
galaxies = [line.strip().split(',') for line in f.readlines()]
for galaxy in galaxies:
    galaxy[1] = int(galaxy[1])
    galaxy[2] = int(galaxy[2])
    galaxy[3] = int(galaxy[3])


def distance(x1,y1,x2,y2):
    return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)

# utility(X) = (benefit(X))^(2) - ((distance(X) + 36) // 3))
# Y-38211325,-1980,1146,4948
def utility(galaxy,sx,sy):
    benefit = galaxy[3]
    x,y = galaxy[1],galaxy[2]
    return benefit**2 - ((distance(sx,sy,x,y) + 36) // 3)

max_utility = 0
max_galaxies = None,None
for i in range(0,len(galaxies)):
    galx,galy = galaxies[i][1],galaxies[i][2]
    utility1 = utility(galaxies[i],0,0)
    for j in range(i+1,len(galaxies)):
        tot_utility = utility1 + utility(galaxies[j],galx,galy)
        if tot_utility > max_utility:
            max_utility = tot_utility
            max_galaxies = galaxies[i][0],galaxies[j][0]


print max_utility
print max_galaxies


# galaxy1 = ["B-142325X", "30","40", "200"]
# galaxy2 = ["P-44123C", "-10","40", "300"]

# print utility(galaxy1,0,0)
# print utility(galaxy2,int(galaxy1[1]),int(galaxy1[2]))
 