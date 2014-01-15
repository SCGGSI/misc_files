from win32com.client import Dispatch
xl = Dispatch('Excel.Application')
vals = xl.Workbooks[0].ActiveSheet.UsedRange()

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

appn_dict = AutoVivification()

for i in range(len(vals)):
	if vals[i][0] is not None:
		if vals[i][0][:4] == 'Appr' and vals[i][0] <> 'Appropriations:':
			appn = vals[i][0][-8:]
			j = 2
			while vals[i + 1][j] is not None:
				j += 1
				if j == 27:
					break
			j -= 1
			k = i + 2
			while vals[k][0] is not None:
				if vals[k][j] is not None:
					line = vals[k][0]
					if line in appn_dict[appn].keys():
						appn_dict[appn][line] += \
								vals[k][j]
					else:
						appn_dict[appn][line] = \
								vals[k][j]
				k += 1
				if k == 11485:
					break

f = open('lines.txt', 'w')

total_sum = 0

for appn in appn_dict.keys():
	for line in appn_dict[appn].keys():
		f.write(appn + '\t' + line + '\t' + \
				str(appn_dict[appn][line]) + '\n')
	print appn + '\t' + str(sum(appn_dict[appn].values()))
	total_sum += sum(appn_dict[appn].values())

print 'total sum is', total_sum

f.close()

print 'Done.'
