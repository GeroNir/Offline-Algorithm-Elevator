import csv
import sys

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


def timeForList(currElev, e):
    floorTime = e['_openTime'] + e['_closeTime'] + e['_startTime'] + e['_stopTime']
    speed = e['_speed']
    total = 0
    for c in range(len(tmpCalls[currElev]) - 1):
        total = total + (abs(int(tmpCalls[currElev][c + 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
    return total


def calculateTime(tmpCall, e, currTime, currElev):
    floorTime = e['_openTime'] + e['_closeTime'] + e['_startTime'] + e['_stopTime']
    speed = e['_speed']
    src = int(tmpCall.src)
    dest = int(tmpCall.dest)
    total = 0

    if (len(tmpCalls[currElev]) > 0):
        for c in range(1, len(tmpCalls[currElev]) + 1):
            total = total + (abs(int(tmpCalls[currElev][c - 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
            endTime = total + currTime
            if (endTime < float(tmpCall.time)):
                tmpCalls[currElev].insert(c + 1, tmpCall.src)
                print(tmpCalls)
                index = c + 1
                break

        if (index + 1 == len(tmpCalls[currElev])):
            minTimeSrc = endTime
        else:
            minTimeSrc = sys.float_info.max
        print(minTimeSrc)
        for i in range(index + 1, len(tmpCalls[currElev])):
            tmpCalls[currElev].remove(tmpCall.src)
            print(tmpCalls)
            tmpCalls[currElev].insert(i, tmpCall.src)
            print(tmpCalls)
            endTime = timeForList(currElev, e) + currTime
            if (endTime < minTimeSrc):
                minTimeSrc = endTime
                index = i
        tmpCalls[currElev].remove(tmpCall.src)
        print(tmpCalls)
        tmpCalls[currElev].insert(index, tmpCall.src)
        print(tmpCalls)

        total = 0
        # find the best insert for dest
        for c in range(1, len(tmpCalls[currElev]) + 1):
            total = total + (abs(int(tmpCalls[currElev][c - 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
            endTime = total + currTime
            if (endTime < float(tmpCall.time)):
                tmpCalls[currElev].insert(c + 1, tmpCall.dest)
                print(tmpCalls)
                index = c + 1
                break

        if (index + 1 == len(tmpCalls[currElev])):
            minTimeDest = endTime
        else:
            minTimeDest = sys.float_info.max
        for i in range(index + 1, len(tmpCalls[currElev])):
            tmpCalls[currElev].remove(tmpCall.dest)
            print(tmpCalls)
            tmpCalls[currElev].insert(i, tmpCall.dest)
            print(tmpCalls)
            endTime = timeForList(currElev, e) + currTime
            if (endTime < minTimeDest):
                minTimeDest = endTime
                index = i
        tmpCalls[currElev].remove(tmpCall.dest)
        print(tmpCalls)
        tmpCalls[currElev].insert(index, tmpCall.dest)
        print(tmpCalls)
        return minTimeDest + minTimeSrc

    else:
        tmpCalls[currElev].append(tmpCall.src)
        tmpCalls[currElev].append(tmpCall.dest)
        total = (abs(src - dest) / speed) + floorTime
        return total + currTime


class OfflineAlgo:
    call_file = 'Ex1_input/Ex1_Calls/Calls_a.csv'
    building_file = 'Ex1_input/Ex1_Buildings/B2.json'
    numOfCalls = Call.Call(call_file, 1).numOfCalls
    numOfElev = Building.Building(building_file).numOfElevators
    b = Building.Building(building_file)

    for c in range(1, numOfCalls + 1):
        tmpCall = Call.Call(call_file, c)
        currTime = 5
        i = 0
        minTime = sys.float_info.max
        print(tmpCalls)
        for e in b.Elevators:
            elevTime = calculateTime(tmpCall, e, currTime, i)
            if (elevTime < minTime):
                minTime = elevTime
                index = i
                print(minTime)
            i += 1

        tmpCall.allocatedTo = index

    if (numOfElev == 1):
        f = open('C:/Users/Hagai/PycharmProjects/OOP_course/newfile.csv', 'a', newline='')
        writer = csv.writer(f)
        row = ['Elevator call', tmpCall.time, tmpCall.src, tmpCall.dest, tmpCall.allocatedto, e['_id']]
        writer.writerow(row)
        f.close()
    print(tmpCalls)
