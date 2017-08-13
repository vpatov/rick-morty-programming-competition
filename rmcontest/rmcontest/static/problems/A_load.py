galaxies = {}
for line in open('problem1_input.txt','r'):
	parts = map(str.strip,line.split(','))
	name,x,y,benefit = parts
	galaxies[name] = {"x":int(x), "y":int(y), "benefit": int(benefit)}

galaxies = []
for line in open('problem1_input.txt','r'):
	parts = map(str.strip,line.split(','))
	name,x,y,benefit = parts
	galaxies.append((name,int(x),int(y),int(benefit)))
