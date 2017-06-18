import math

t_nums = [0,1,3,]
nums = [0,1,6]
n = 5823


def t(n):
	return t_nums[n]

def gen_t(n):
	global t_nums
	i = 3
	t_nums = t_nums + ([0] * (n-len(t_nums) + 1))
	while (i <= n):
		t_nums[i] = t_nums[i-1] + i
		i += 1

def gen_s(n):
	global nums
	i = 3
	nums = nums + ([0] * (n-len(nums) + 1))
	while(i <= n):
		nums[i] = abs((nums[i-1] - (t_nums[i-1] * (nums[i-1]//5))) + (nums[i-2]))
		i += 1

gen_t(n)
gen_s(n)

print nums[n-1] % 1000000

