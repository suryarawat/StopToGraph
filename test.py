import urllib.request,json
import time
from datetime import datetime
import matplotlib.pyplot as plt

# #collect the schedule time and then compare it to the real time of the bus
listStops = {} #dictionary of all the stops in route 36
scheduleDict = {} #dictionary of all the scheduled stops of the corressponding stops
def getScheduleTime(listStops, scheduleDict):
    reqCounter = 0
    url = "https://api.winnipegtransit.com/v3/stops.json?api-key=Iy86KOGosL28zxOLSAc2&route=36"
    reqCounter += 1
    res = urllib.request.urlopen(url)
    res = res.read()
    jsonObj = json.loads(res)
    print (jsonObj)
    for i in range (0, len(jsonObj["stops"])):
        scheduleUrl = "https://api.winnipegtransit.com/v3/stops/"+str(jsonObj["stops"][i]["key"])+"/schedule.json?api-key=Iy86KOGosL28zxOLSAc2&route=36&start=2019-09-13T04:00&end=2019-09-13T20:00"
        reqCounter += 1
        response = urllib.request.urlopen(scheduleUrl)
        jsonSchedule = json.loads(response.read())
        print(reqCounter)
        if (reqCounter > 98):
            time.sleep(61)
            reqCounter = 0
        tempList = []
        if (len(jsonSchedule["stop-schedule"]["route-schedules"]) > 0):
            for j in range (0, len(jsonSchedule["stop-schedule"]["route-schedules"][0]["scheduled-stops"])):
                tempList.append(jsonSchedule["stop-schedule"]["route-schedules"][0]["scheduled-stops"][j]["times"])
        scheduleDict[i] = tempList
        listStops[jsonObj["stops"][i]["name"]] = scheduleDict
    print(scheduleDict)
    return listStops, scheduleDict
 
estDepart = {}
schDepart = {}

listStops,scheduleDict = getScheduleTime(listStops, scheduleDict)

for i in range(len(scheduleDict)):
     tempList = scheduleDict[i]
     tempList2 = []
     tempList3 = []
     for j in range(len(tempList)):
         tempList2.append(tempList[j]["departure"]["scheduled"])
         tempList2[j] = tempList2[j][tempList2[j].find('T') + 1:]
         tempList3.append(tempList[j]["departure"]["estimated"])
         tempList3[j] = tempList3[j][tempList3[j].find('T') + 1:]

     schDepart[i] = tempList2
     estDepart[i] = tempList3
print(schDepart)
file = open("list of stops.txt","w+")

file.write(str(listStops.keys()))
file.close()
file1 = open("scheduled stops departure.txt","w+")
for i in range(0, len(schDepart)):
    file1.write(str(schDepart[i]))
file1.close()
file2 = open("estimated stops departure.txt", "w+")
for i in range(0, len(estDepart)):
    file2.write(str(estDepart[i]))
file2.close()
file = open("list of stops.txt", "r")
fileContent = str(file.read())[12:-3]


newList = list(fileContent.split("', '"))


file.close()
file = open("scheduled stops departure.txt", "r")
stops = str(file.read())[1:-1]
times = list(stops.split("][",))
file.close()
yAxis = []
for item in times:
    item = item[1:-1]
    list1 = list(item.split("', '"))
    yAxis.append(list1)
for y in yAxis:
    for yy in y:
        if yy != '':
            datetime.strptime(yy, '%H:%M:%S')
print(yAxis)
print(len(newList))

for i in range(len(newList)):
    for y in yAxis[i]:
        plt.scatter(newList[i],y)
    plt.gcf().autofmt_xdate()
    plt.savefig("plt"+str(i)+".png")
    plt.show()


