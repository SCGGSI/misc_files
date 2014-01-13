import numpy as np

def CountSick():
	SickCount = []
	
	for Area in Areas:
		SickCount.append(np.bincount(popInd['Location'])[Area] - (CountWell()[Area - 1]))
		

	return SickCount

def CountWell():
	WellCount = []
	
	for Area in Areas:
		WellCount.append(np.bincount(popInd[np.logical_and(popInd['Location'] == Area, popInd['Health'] == 0)]['Health']))

	return WellCount

Areas = [1, 2, 3]

b = []
for i in range(1, 101):
	randnum = np.random.randint(1, 101)

	if randnum <= 3:
		b.append(1)
	else:
		b.append(0)

c = [np.random.randint(1, 4) for i in range(1, 101)]

d = []
for each in b:
    if each == 1:
        d.append(0)
    else:
        d.append(-1)

dt = np.dtype([('Health', np.int8), ('Location', np.int8), ('Days', np.int8)])
Person = zip(b, c, d)

popInd = np.array(Person, dt)

print CountWell()[0]
print CountSick()[0]

for i in range(1, 6):
        print "Time step:", i
        for each in popInd[popInd['Location'] == 1]:
                print each
                if each['Health'] == 1:
                        each['Days'] = each['Days'] + 1

        
