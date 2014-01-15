def factors(n):
	return set(reduce(list.__add__,
		([i, n // i] for i in range(1, int(n ** 0.5) + 1) 
			if n % i == 0 and i != n)))

numbers = []

for i in range(2, 10):
	print i, factors(i)
	numbers.append((i, sum(factors(i))))


print numbers[0]

