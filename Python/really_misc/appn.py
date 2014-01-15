from win32com.client import Dispatch
xl = Dispatch('Excel.Application')
vals = xl.Workbooks[0].ActiveSheet.UsedRange()

appn_dict = {}

for i in range(len(vals)):
	if vals[i][0] is not None:
		if vals[i][0][:4] == 'Appr' and vals[i][0] <> 'Appropriations:':
			appn = vals[i][0][-8:]
			appn_sum = 0
			j = 2
			while vals[i + 1][j] is not None:
				j += 1
				if j == 27:
					break
			j -= 1
			k = i + 2
			while vals[k][0] is not None:
				if vals[k][j] is not None:
					appn_sum += vals[k][j]
				k += 1
				if k == 11485:
					break
			appn_dict[appn] = appn_sum

total_sum = 0

f = open('appn_lines.txt', 'w')

for each in appn_dict.keys():
	print each + '\t' + str(appn_dict[each])
	f.write(each + '\t' + str(appn_dict[each]) + '\n')
	total_sum += appn_dict[each]

f.close()

print '\n\nTotal sum is', str(total_sum)
