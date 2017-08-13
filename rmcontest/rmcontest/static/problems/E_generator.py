import random
import string
import sys
import json


sys.setrecursionlimit(sys.getrecursionlimit()*3)

keys = []
for i in string.uppercase:
    for j in string.uppercase:
        for k in string.uppercase:
            keys.append(i+j+k)

random.shuffle(keys)
keys.remove("RMC")

tree = {"RMC":{}}



def populate(root,limit,nary):
    global keys
    if limit == 0:
        return
    branches = nary - random.randint(0,nary-1)
    for i in range(0,nary):
        if not len(keys):
            return
        next_key = keys.pop()
        root[next_key] = {}
        if random.randint(1,3) == 1:
            populate(root[next_key],limit - 1,nary)

populate(tree['RMC'],25,4)
f = open('problem5_input.json','w')
json.dump(tree,f)
f.close()


