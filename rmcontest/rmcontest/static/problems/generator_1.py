import random
f = open('input_7.txt','w')

out = ""
level = 0
for i in range(0,random.randint(400,500)):
	if (level > 0):
		if random.randint(0,1) == 1:
			out += '>'
			level -= 1
		else:
			out += '<'
			level += 1
	else:
		out += '<'
		level += 1

while (level != 0):
	out += '>'
	level -= 1

f.write(out)
f.close()