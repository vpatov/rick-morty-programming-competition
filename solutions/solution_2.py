def get_solution(f=None):
    return sum([num for num in range(1,(10**6) + 1) if num % sum([int(digit) for digit in str(num)]) == 0])

