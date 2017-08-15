def get_solution(f=None):
	import math

	t_nums = [0,1,3,]
	nums = [0,1,6]
	n = 5823

	## gen t_nums
	i = 3
	t_nums = t_nums + ([0] * (n-len(t_nums) + 1))
	while (i <= n):
		t_nums[i] = t_nums[i-1] + i
		i += 1

	# gen shleeble nums
	i = 3
	nums = nums + ([0] * (n-len(nums) + 1))

	while(i <= n):
		nums[i] = (nums[i-2] - (t_nums[i-1] * (nums[i-1]*11))) 
		i += 1


	return nums[n-1] % 1000000




