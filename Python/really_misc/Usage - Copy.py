import psutil as psu

procList = psu.get_pid_list()

procList2 = []
for proc in procList:
    procList2.append(psu.Process(proc))

procList = procList2

newList = []

for proc in procList:
    try:
        newList.append((proc.name, proc.username, proc.get_memory_percent(), proc.get_open_files()))

    except:
	newList.append((proc.name, 'Access Denied', proc.get_memory_percent(),'Access Denied'))
		
newList.sort(key = lambda newList: newList[2], reverse = True)

names = []
for each in newList:
    names.append(each[0])

users = []
for each in newList:
    users.append(each[1])

usage = []
for each in newList:
    usage.append(each[2])

files = []
for each in newList:
    files.append(each[3])

filecounts = []
for each in files:
    test3 = str(each).split()
    count = 0
    for i in test3:
    	if 'openfile' in i:
    		count += 1
    if count == 0:
	count = 'Access Denied'
    filecounts.append(count)

ext_file = open("Output.csv", "w")
ext_file.write("File Name|User Name|CPU Usage (Percent)|Files Opened by Process|Count of Files")

for i in range(0, len(names)):
    ext_file.write(str(names[i]) + "|" + str(users[i]) + "|" + str(usage[i]) + "|" + str(files[i]) + "|" + str(filecounts[i]))

ext_file.close()
