import csv
import sys
import Building
import Call
import time


# This function calculate the time for a specific list, for each elevator
def timeForList(e):
    tmpCalls = [row[:] for row in calls]
    floorTime = e['_openTime'] + e['_closeTime'] + e['_startTime'] + e['_stopTime']
    speed = e['_speed']
    total = 0
    currElev = e['_id']
    for c in range(len(tmpCalls[currElev]) - 1):
        total = total + (abs(int(tmpCalls[currElev][c + 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
    return total


# This function get the call and the elevator, find the place that from him we want to insert.
# and check for every place till the end. then, we choose the place that add the minimum time
def calculateTime(tmpCall, e, currTime, startIndx):
    tmpCalls = [row[:] for row in calls]
    floorTime = e['_openTime'] + e['_closeTime'] + e['_startTime'] + e['_stopTime']
    speed = e['_speed']
    currElev = e['_id']
    src = int(tmpCall.src)
    dest = int(tmpCall.dest)
    total = 0
    timeBeforeAdd = timeForList(e) + currTime
    index = len(tmpCalls[currElev])
    if (len(tmpCalls[currElev]) > 0):  # check if the list isn't empty
        for c in range(startIndx,
                       len(tmpCalls[currElev])):  # goes all over the list and check where we want to start the inserts
            total = total + (abs(int(tmpCalls[currElev][c - 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
            endTime = total + currTime
            if (endTime > float(tmpCall.time)):
                index = c
                startIndx = c

        minTimeSrc = timeForList(e) + currTime

        # find the best insert for source
        for i in range(index, int(len(
                tmpCalls[currElev]) - index / 2)):  # check for the insert that add the minimal to the time
            tmpCalls[currElev].insert(i, tmpCall.src)
            totalTime = timeForList(e) + currTime
            if (totalTime < minTimeSrc):
                minTimeSrc = totalTime
                index = i
            del tmpCalls[currElev][i]
        tmpCalls[currElev].insert(index, tmpCall.src)
        indxSrc = index

        # find the best insert for destination
        total = 0
        index = len(tmpCalls[currElev])
        for c in range(index,
                       len(tmpCalls[currElev])):  # goes all over the list and check where we want to start the inserts
            total = total + (abs(int(tmpCalls[currElev][c - 1]) - int(tmpCalls[currElev][c])) / speed) + floorTime
            endTime = total + currTime
            if (endTime > float(tmpCall.time)):
                index = c
        minTimeDest = timeForList(e) + currTime

        for i in range(index, int(len(
                tmpCalls[currElev]) - index / 2)):  # check for the insert that add the minimal to the time
            tmpCalls[currElev].insert(i, tmpCall.dest)
            totalTime = timeForList(e) + currTime
            if (totalTime < minTimeDest):
                minTimeDest = totalTime
                index = i
            del tmpCalls[currElev][i]
        tmpCalls[currElev].insert(index, tmpCall.dest)
        return minTimeDest + minTimeSrc - timeBeforeAdd, indxSrc, index, startIndx

    else:
        tmpCalls[currElev].append(tmpCall.src)
        tmpCalls[currElev].append(tmpCall.dest)
        total = (abs(src - dest) / speed) + floorTime
        return total + currTime, 0, 1, startIndx


def allocateElev(Building_file, Calls_file, Calls_out):
    start = time.time()
    numOfCalls = Call.Call(Calls_file, 1).numOfCalls
    b = Building.Building(Building_file)
    global calls
    calls = []
    global tmpCalls
    tmpCalls = []
    fastestSpeed = b.Elevators[0]['_speed']
    fastElevID = 0
    startIndx = 1
    for e in b.Elevators:  # This loop find the fastest elevator
        calls.insert(0, [])
        tmpCalls.insert(0, [])
        if e['_speed'] > fastestSpeed:
            fastElevID = e['_id']
            fastestSpeed = e['_speed']
    f = open(Calls_out, 'w', newline='')
    currTime = int(float(Call.Call(Calls_file, 1).time)) + 1
    for c in range(1,
                   numOfCalls + 1):  # This loop roll all over the calls and the elevators, and find for every call the fastest elevator
        tmpCall = Call.Call(Calls_file, c)
        i = 0
        src = int(tmpCall.src)
        dest = int(tmpCall.dest)
        minTime = sys.float_info.max
        index = 0
        for e in b.Elevators:  # roll all over the elevators
            elevTime, indxSrc, indxDest, startIndx = calculateTime(tmpCall, e, currTime, startIndx)
            if (e['_id'] == fastElevID and abs(src - dest) >= (b.maxFloor - b.minFloor + 1) / 2):
                if (elevTime < minTime):
                    minTime = elevTime
                    index = e['_id']
            elif (e['_id'] != fastElevID):
                if (elevTime < minTime):
                    minTime = elevTime
                    index = e['_id']
            i += 1

        tmpCall.allocatedTo = index
        calls[index].insert(indxSrc, tmpCall.src)
        calls[index].insert(indxDest, tmpCall.dest)

        # Writing to the csv file
        writer = csv.writer(f)
        row = ['Elevator call', tmpCall.time, tmpCall.src, tmpCall.dest, 0, tmpCall.allocatedTo]
        writer.writerow(row)
    f.close()
    end = time.time()

    print("Running time: ", end - start)
