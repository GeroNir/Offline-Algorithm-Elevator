import unittest
import Call
import csv
import random
import OfflineAlgo

class Test(unittest.TestCase):
    def testRandomCase(self):
        call_file = 'Ex1_input/Ex1_Calls/Calls_b.csv'
        f = open('C:/Users/Hagai/PycharmProjects/OOP_course/rndFile.csv', 'a', newline='')

        for i in range(1, 1001):
            tmpCall = Call.Call(call_file, i)
            writer = csv.writer(f)
            row = ['Elevator call', tmpCall.time, tmpCall.src, tmpCall.dest, 0, random.randint(0, 4)]
            writer.writerow(row)
        f.close()

'''
tmpCall = Call('Ex1_input/Ex1_Calls/Calls_a.csv', 3)
print(tmpCall.time)
print(tmpCall.numOfCalls)

#run from command line Using sys
# def hello(a,b):
#     print ("hello and that's your sum:", a + b)
#
# if __name__ == "__main__":
#     a = int(sys.argv[1])
#     b = int(sys.argv[2])
#     hello(a, b)


# open the file in the write mode
f = open('C:/Users/Hagai/PycharmProjects/OOP_course/new1.csv', 'a')

# create the csv writer
writer = csv.writer(f)

# write a row to the csv file
list = ['this', 'is']
writer.writerow(list)

# close the file
f.close()


import Building as b
b1 = b.Building('Ex1_input/Ex1_Buildings/B1.json')
print("MinFloor is: ", b1.minFloor)
print(b1.Elevators[0]['_id'])
print(b1.Elevators)
print(b1.numOfElevators)

# import json
#
# with open('Ex1_input/Ex1_Buildings/B2.json') as b1:
#     data = json.load(b1)
# print(data['_minFloor'])

list = [3, 5, 7]
for floor in range(len(list)-1):
    print(list.__getitem__(floor+1) - list.__getitem__(floor))



list = [[], []]
list[0].append(4)
list[1].append(4)
print(list)
del list [0][0]
print(list)


call_file = 'Ex1_input/Ex1_Calls/Calls_b.csv'
f = open('C:/Users/Hagai/PycharmProjects/OOP_course/rndFile.csv', 'a', newline='')

for i in range(1,1001):
    tmpCall = Call.Call(call_file, i)
    writer = csv.writer(f)
    row = ['Elevator call', tmpCall.time, tmpCall.src, tmpCall.dest, 0, random.randint(0,4)]
    writer.writerow(row)

f.close()
'''
