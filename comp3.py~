# Rick is trying to calibrate his portal gun to get him and Morty to Alpha-Betrium, 
# so that he can collect some money that Magma-Q owes him from an old bet (41 shmeckles is 
# no petty change, thats $6068 USD!). His dial isn't working properly, so he has to configure 
# the destination manually. To do this, he needs to generate the 29234th shleeble number. 

# The formula for the nth shleeble number shleeble(n) = (T(n) * floor(shleeble(n-1) / 5)) - (shleeble(n+1)) + shleeble(n-2) * sheeble(floor(n/2))

import math
import numpy as np

t_nums = [0,1,3,]
nums = [0,1,6]

n = 13817
n = 29234


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
		nums[i] = ((nums[i-1] - (t_nums[i-1] * (nums[i-1]//5))) + (nums[i-2]))
		i += 1

gen_t(n)
gen_s(n)
