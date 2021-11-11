import csv

import Building
import Call

calls = [[], []]
tmpCalls = [[], []]

'''
def calculateTime2(tmpCall, e):
    floorTime = e['_openTime'] + e['_closeTime'] + e['_startTime'] + e['_stopTime']
    speed = e['_speed']
    src = tmpCall.src
    dest = tmpCall.dest
    tmpUpCalls = upCalls
    tmpDownCalls = downCalls
    if(timeline.__getitem__(len(timeline)) < tmpCall.time):
        callTime = tmpCall.time + abs( + abs((tmpCall.src - tmpCall.dest)/speed)
        timeline.append(callTime)
'''


# TODO: func that check wheater the elevator need to wait
def calculateTime(tmpCall, e, currTime, currElev):
    floorTime = e['_openTime'] + e['_closeTime'] + e['_startTime'] + e['_stopTime']
    speed = e['_speed']
    src = int(tmpCall.src)
    dest = int(tmpCall.dest)
    total = 0

    # TODO: consider waiting time on floor
    # TODO: consider start time

    isGet = True
    if (len(tmpCalls[currElev]) > 0):
        for c in range(len(tmpCalls[currElev]) - 1):
            total = total + (abs(int(tmpCalls[currElev][c + 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
            endTime = total + currTime
            if (endTime < float(tmpCall.time) and isGet):
                tmpCalls[currElev].insert(c+1, tmpCall.src)
                print(tmpCalls)
                index = c
                isGet = False
        minTimeSrc = 9999

        for i in range(index + 1, len(tmpCalls[currElev]) - 1):

            tmpCalls[currElev].remove(tmpCall.src)
            tmpCalls[currElev].insert(i, tmpCall.src)
            total = total + (abs(int(tmpCalls[currElev][i + 1]) - int(tmpCalls[currElev][i])) / speed) + floorTime
            if (total < minTimeSrc):
                minTimeSrc = total
                index = i
        tmpCalls[currElev].remove(tmpCall.src)
        tmpCalls[currElev].insert(index+1, tmpCall.src)
        isGet = True

        # add the dest in the right place
        for c in range(len(tmpCalls[currElev]) - 1):
            total = total + (abs(int(tmpCalls[currElev][c + 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
            endTime = total + currTime
            if (endTime < float(tmpCall.time) and isGet):
                tmpCalls[currElev].insert(c+1, tmpCall.dest)
                index = c
                isGet = False
        minTimeDest = total

        for i in range(index + 1, len(tmpCalls[currElev])-1):
            total = 0
            tmpCalls[currElev].remove(tmpCall.dest)
            tmpCalls[currElev].insert(i, tmpCall.dest)
            total = total + (abs(int(tmpCalls[currElev][i + 1]) - int(tmpCalls[currElev][i])) / speed) + floorTime
            if (total < minTimeDest):
                minTimeDest = total
                index = i
        tmpCalls[currElev].remove(tmpCall.dest)
        tmpCalls[currElev].insert(index, tmpCall.dest)
        return minTimeDest + minTimeSrc
    else:
        tmpCalls[currElev].append(tmpCall.src)
        tmpCalls[currElev].append(tmpCall.dest)
        total = (abs(src-dest) / speed) + floorTime
        return total + currTime
class OfflineAlgo:
    call_file = 'Ex1_input/Ex1_Calls/Calls_a.csv'
    building_file = 'Ex1_input/Ex1_Buildings/B2.json'
    numOfCalls = Call.Call(call_file, 1).numOfCalls
    numOfElev = Building.Building(building_file).numOfElevators
    b = Building.Building(building_file)
    c = 1
    for c in range(1, numOfCalls+1):
        tmpCall = Call.Call(call_file, c)
        currTime = 5
        i = 0
        minTime = 99999 #TODO: change to max value
        #print(tmpCalls)
        for e in b.Elevators:
            elevTime = calculateTime(tmpCall, e, currTime, i)
            i += 1
            if(elevTime < minTime):
                minTime = elevTime
                print(minTime)

    if (numOfElev == 1):
        f = open('C:/Users/Hagai/PycharmProjects/OOP_course/newfile.csv', 'a', newline='')
        writer = csv.writer(f)
        row = ['Elevator call', tmpCall.time, tmpCall.src, tmpCall.dest, 0, e['_id']]
        writer.writerow(row)
        f.close()
    print(tmpCalls)