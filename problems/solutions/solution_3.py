def get_solution(f=None):
    import math
    galaxies = [line.strip().split(',') for line in f.readlines()]
    for galaxy in galaxies:
        galaxy[1] = int(galaxy[1])
        galaxy[2] = int(galaxy[2])
        galaxy[3] = int(galaxy[3])


    def distance(x1,y1,x2,y2):
        return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)


    def utility(galaxy,sx,sy):
        benefit = galaxy[3]
        x,y = galaxy[1],galaxy[2]
        return benefit**2 - ((distance(sx,sy,x,y) + 36) // 3)

    max_utility = 0
    max_galaxies = None,None
    for i in range(0,len(galaxies)):
        galx,galy = galaxies[i][1],galaxies[i][2]
        utility1 = utility(galaxies[i],0,0)
        for j in range(0,len(galaxies)):
            tot_utility = utility1 + utility(galaxies[j],galx,galy)
            if tot_utility > max_utility:
                max_utility = tot_utility
                max_galaxies = galaxies[i][0],galaxies[j][0]






    return int(max_utility)

if __name__ == '__main__':
    print(get_solution(open('prob3_in.txt','r')))

