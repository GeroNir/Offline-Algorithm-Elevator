import Building
import Call

upCalls = ['']
downCalls = ['']


# TODO: func that check wheater the elevator need to wait
def calculateTime(tmpCall, e):
    ans = 0
    floorTime = e['_openTime'] + e['_closeTime'] + e['_startTime'] + e['_stopTime']
    speed = e['_speed']
    src = tmpCall.src
    dest = tmpCall.dest
    tmpUpCalls = upCalls
    tmpDownCalls = downCalls

    # TODO: consider waiting time
    if (len(upCalls) > 0):
        for floor in range(len(upCalls) - 1):
            timeUp = timeUp + (abs(list.__getitem__(floor + 1) - list.__getitem__(floor)) / speed) + floorTime
    if (len(downCalls) > 0):
        for floor in range(len(downCalls) - 1):
            timeDown = timeDown + (abs(list.__getitem__(floor + 1) - list.__getitem__(floor)) / speed) + floorTime

    #if (tmpCall.status == 1):


# print(dest)


class OfflineAlgo:
    call_file = 'Ex1_input/Ex1_Calls/Calls_a.csv'
    building_file = 'Ex1_input/Ex1_Buildings/B1.json'
    numOfCalls = Call.Call(call_file, 1).numOfCalls
    numOfElev = Building.Building(building_file).numOfElevators
    b = Building.Building(building_file)
    c = 1
    for c in range(1, numOfCalls):
        tmpCall = Call.Call(call_file, c)
        for e in b.Elevators:
            # print(e)
            calculateTime(tmpCall, e)
