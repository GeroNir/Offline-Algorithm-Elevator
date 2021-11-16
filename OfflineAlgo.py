import csv
import sys
import Building
import Call
import unittest

def timeForList(e):
    tmpCalls = [row[:] for row in calls]
    floorTime = e['_openTime'] + e['_closeTime'] + e['_startTime'] + e['_stopTime']
    speed = e['_speed']
    total = 0
    currElev = e['_id']
    for c in range(len(tmpCalls[currElev]) - 1):
        total = total + (abs(int(tmpCalls[currElev][c + 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
    return total

def calculateTime(tmpCall, e, currTime):

    tmpCalls = [row[:] for row in calls]
    floorTime = e['_openTime'] + e['_closeTime'] + e['_startTime'] + e['_stopTime']
    speed = e['_speed']
    currElev = e['_id']
    src = int(tmpCall.src)
    dest = int(tmpCall.dest)
    total = 0
    timeBeforeAdd = timeForList(e) + currTime

    index = len(tmpCalls[currElev])
    if (len(tmpCalls[currElev]) > 0):
        for c in range(startIndx, len(tmpCalls[currElev])):
            total = total + (abs(int(tmpCalls[currElev][c - 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
            endTime = total + currTime
            if (endTime > float(tmpCall.time)):
                index = c
                startIndx = c
                break

        minTimeSrc = timeForList(e) + currTime
        # print(minTimeSrc)

        for i in range(index, len(tmpCalls[currElev])):
            tmpCalls[currElev].insert(i, tmpCall.src)
            # print(tmpCalls)
            totalTime = timeForList(e) + currTime
            if (totalTime < minTimeSrc):
                minTimeSrc = totalTime
                index = i
            del tmpCalls[currElev][i]
        # print(tmpCalls)
        tmpCalls[currElev].insert(index, tmpCall.src)
        # print(tmpCalls)
        indxSrc = index
        # find the best insert for dest
        total = 0
        index = len(tmpCalls[currElev])
        for c in range(index, len(tmpCalls[currElev])):
            total = total + (abs(int(tmpCalls[currElev][c - 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
            endTime = total + currTime
            if (endTime > float(tmpCall.time)):
                index = c
                break

        minTimeDest = timeForList(e) + currTime

        for i in range(index, len(tmpCalls[currElev]) + 1):
            tmpCalls[currElev].insert(i, tmpCall.dest)
            # print(tmpCalls)
            totalTime = timeForList(e) + currTime
            if (totalTime < minTimeDest):
                minTimeDest = totalTime
                index = i
            del tmpCalls[currElev][i]
        # print(tmpCalls)
        tmpCalls[currElev].insert(index, tmpCall.dest)
        # print(tmpCalls)
        return minTimeDest + minTimeSrc - timeBeforeAdd, indxSrc, index

    else:
        tmpCalls[currElev].append(tmpCall.src)
        tmpCalls[currElev].append(tmpCall.dest)
        total = (abs(src - dest) / speed) + floorTime
        return total + currTime, 0, 1

class OfflineAlgo:
    # TODO: run from command line
    # TODO: initialize the lists with the parm of calls and eletaors

    call_file = 'Ex1_input/Ex1_Calls/Calls_d.csv'
    building_file = 'Ex1_input/Ex1_Buildings/B4.json'
    numOfCalls = Call.Call(call_file, 1).numOfCalls
    numOfElev = Building.Building(building_file).numOfElevators
    b = Building.Building(building_file)
    global calls
    calls = [[], [], [], [], [], [], [], [], [], []]
    global tmpCalls
    tmpCalls = [[], [], [], [], [], [], [], [], [], []]
    fastestSpeed = b.Elevators[0]['_speed']
    fastElevID = 0
    startIndx = 0
    for e in b.Elevators:
        if e['_speed'] > fastestSpeed:
            fastElevID = e['_id']
            fastestSpeed = e['_speed']
    f = open('C:/Users/Hagai/PycharmProjects/OOP_course/newfile.csv', 'a', newline='')
    currTime = int(float(Call.Call(call_file, 1).time)) + 1
    for c in range(1, numOfCalls + 1):
        tmpCall = Call.Call(call_file, c)
        i = 0
        src = int(tmpCall.src)
        dest = int(tmpCall.dest)
        minTime = sys.float_info.max
        index = 0
        print(c)
        for e in b.Elevators:
            elevTime, indxSrc, indxDest = calculateTime(tmpCall, e, currTime)
            if (e['_id'] == fastElevID and abs(src-dest) >= (b.maxFloor - b.minFloor + 1)/2):
                if (elevTime < minTime):
                    minTime = elevTime
                    index = e['_id']
                # print(minTime)
            elif (e['_id'] != fastElevID):
                if (elevTime < minTime):
                    minTime = elevTime
                    index = e['_id']
            i += 1


        tmpCall.allocatedTo = index
        # print(calls)
        calls[index].insert(indxSrc, tmpCall.src)
        calls[index].insert(indxDest, tmpCall.dest)
        # print(calls)


        writer = csv.writer(f)
        row = ['Elevator call', tmpCall.time, tmpCall.src, tmpCall.dest, 0, tmpCall.allocatedTo]
        writer.writerow(row)
    f.close()