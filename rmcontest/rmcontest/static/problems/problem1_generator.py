import random

capital_letters = [chr(i) for i in range(ord('A'),ord('Z') + 1)]

def gen_galaxy():
    name = random.choice(capital_letters) + '-' \
    + random.choice('123456789') \
    + ''.join([random.choice('123456789') for i in range(7)])
    x,y = random.randint(-3000,3000),random.randint(-3000,3000)
    benefit = random.randint(50,10000)
    return ','.join((name,str(x),str(y),str(benefit)))
    

f = open('galaxies.txt','w')
for i in range(0,90):
    galaxy = gen_galaxy()
    print galaxy
    f.write(galaxy + '\n')

f.close()