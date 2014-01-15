def factorGenerator(n):
	for i in xrange(1,n/2+1):
		if n%i == 0: yield i
	yield n

def divisorGen(n):
	factors = list(factorGenerator(n))
	nfactors = len(factors)
	f = [0] * nfactors
	while True:
		yield reduce(lambda x, y: x*y, [factors[x]**f[x] for x in range(nfactors)], 1)
		i = 0
		while True:
			f[i] += 1
			if f[i] <= factors[i]:
				break
			f[i] = 0
			i += 1
			if i >= nfactors:
				return
