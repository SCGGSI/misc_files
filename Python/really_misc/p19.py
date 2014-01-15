month = 0
year = 1901
weekday = 2
sun_sum = 0

def is_leap_year(year):
	if year % 100 == 0:
		if year % 400:
			return True
		else:
			return False
	elif year % 4 == 0:
		return True
	else:
		return False

month_days = {
	0 : range(31),  # January
	1 : range(28),  # February
	2 : range(31),  # March
	3 : range(30),  # April
	4 : range(31),  # May
	5 : range(30),  # June
	6 : range(31),  # July
	7 : range(31),  # August
	8 : range(30),  # September
	9 : range(31),  # October
	10 : range(30), # Novermber
	11 : range(31)  # December
	}

while year <= 2000:
	for month in range(12):
		if month == 1 and is_leap_year(year):
			days = range(29)
		elif month == 1:
			days = range(28)
		else:
			days = month_days[month]

		for day in days:
			if day == 0 and weekday == 0:
				sun_sum += 1
				print '%s/%s/%s' % (str(month + 1), str(day + 1), str(year))

			weekday = (weekday + 1) % 7
		

	
	year += 1


print 'There were %s sundays on the first of the month!' % str(sun_sum)






