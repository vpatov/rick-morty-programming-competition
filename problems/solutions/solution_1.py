def get_solution(f):
	data = f.read()

	level = 0
	max_level = 0
	for bracket in data:
		if bracket == '<':
			level += 1
			if level > max_level:
				max_level = level
		else:
			level -= 1
	return max_level

if __name__ == '__main__':
	print(get_solution(open('input_1.txt','r')))