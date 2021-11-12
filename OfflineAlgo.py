import csv
import sys
import Building
import Call
import copy


def timeForList(e):
    floorTime = e['_openTime'] + e['_closeTime'] + e['_startTime'] + e['_stopTime']
    speed = e['_speed']
    total = 0
    currElev = e['_id']
    for c in range(len(tmpCalls[currElev]) - 1):
        total = total + (abs(int(tmpCalls[currElev][c + 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
    return total


def calculateTime(tmpCall, e, currTime):
    # TODO: copy the list or remove the rest
    floorTime = e['_openTime'] + e['_closeTime'] + e['_startTime'] + e['_stopTime']
    speed = e['_speed']
    currElev = e['_id']
    src = int(tmpCall.src)
    dest = int(tmpCall.dest)
    total = 0

    if (len(tmpCalls[currElev]) > 0):
        for c in range(1, len(tmpCalls[currElev]) + 1):
            total = total + (abs(int(tmpCalls[currElev][c - 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
            endTime = total + currTime
            if (endTime < float(tmpCall.time)):
                index = c + 1
                break

        if (index == len(tmpCalls[currElev])):
            minTimeSrc = endTime
        else:
            minTimeSrc = sys.float_info.max
        print(minTimeSrc)

        for i in range(index, len(tmpCalls[currElev])+1):
            tmpCalls[currElev].insert(i, tmpCall.src)
            print(tmpCalls)
            totalTime = timeForList(e) + currTime
            if (totalTime < minTimeSrc):
                minTimeSrc = totalTime
                index = i
            del tmpCalls[currElev][i]
        print(tmpCalls)
        tmpCalls[currElev].insert(index, tmpCall.src)
        print(tmpCalls)
        indxSrc = index
        # find the best insert for dest
        total = 0
        for c in range(index, len(tmpCalls[currElev])):
            total = total + (abs(int(tmpCalls[currElev][c - 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
            endTime = total + currTime
            if (endTime < float(tmpCall.time)):
                index = c + 1
                break

        if (index == len(tmpCalls[currElev])):
            minTimeDest = endTime
        else:
            minTimeDest = sys.float_info.max

        for i in range(index, len(tmpCalls[currElev]) + 1):
            tmpCalls[currElev].insert(i, tmpCall.dest)
            print(tmpCalls)
            totalTime = timeForList(e) + currTime
            if (totalTime < minTimeDest):
                minTimeDest = totalTime
                index = i
            del tmpCalls[currElev][i]
        print(tmpCalls)
        tmpCalls[currElev].insert(index, tmpCall.dest)
        print(tmpCalls)
        return minTimeDest + minTimeSrc,indxSrc, index

    else:
        tmpCalls[currElev].append(tmpCall.src)
        tmpCalls[currElev].append(tmpCall.dest)
        total = (abs(src - dest) / speed) + floorTime
        return total + currTime, 0, 1


class OfflineAlgo:
    global calls
    calls = [[], []]
    global tmpCalls
    tmpCalls = [[], []]
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

        index = 0
        for e in b.Elevators:
            elevTime,indxSrc, indxDest = calculateTime(tmpCall, e, currTime)
            if (elevTime < minTime):
                minTime = elevTime
                index = e['_id']
                print(minTime)
            i += 1

        tmpCall.allocatedTo = index
        print(calls)
        calls[index].insert(indxSrc,tmpCall.src)
        calls[index].insert(indxDest, tmpCall.dest)
        print(calls)
        # todo: fix the insert (duplicates)

        if (numOfElev == 1):
            f = open('C:/Users/Hagai/PycharmProjects/OOP_course/newfile.csv', 'a', newline='')
            writer = csv.writer(f)
            row = ['Elevator call', tmpCall.time, tmpCall.src, tmpCall.dest, 0, e['_id']]
            writer.writerow(row)
            f.close()
        else:
            f = open('C:/Users/Hagai/PycharmProjects/OOP_course/newfile.csv', 'a', newline='')
            writer = csv.writer(f)
            row = ['Elevator call', tmpCall.time, tmpCall.src, tmpCall.dest, tmpCall.allocatedTo, e['_id']]
            writer.writerow(row)
            f.close()


