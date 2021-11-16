import unittest
import Call
import csv
import random
import OfflineAlgo
import Building
from csv import reader


class Test(unittest.TestCase):

    def testBuilding(self):
        building_file = 'Ex1_input/Ex1_Buildings/B5.json'
        b = Building.Building(building_file)
        self.assertEqual(10, b.numOfElevators)
        self.assertEqual(-10, b.minFloor)
        self.assertEqual(100, b.maxFloor)

    def testCall(self):
        calls_file = 'Ex1_input/Ex1_Calls/Calls_c.csv'
        call = Call.Call(calls_file, 1)
        self.assertEqual(1000, call.numOfCalls)
        self.assertEqual(-6, int(call.src))
        self.assertEqual(78, int(call.dest))
        self.assertEqual(1, int(call.status))
        self.assertEqual(1, int(call.id))

    def testAllocationRight(self):
        # check That all the allocation is not equal to -1
        calls_file = 'Ex1_input/Ex1_Calls/Calls_b.csv'
        building_file = 'Ex1_input/Ex1_Buildings/B5.json'
        b = Building.Building(building_file)
        isRight = True
        OfflineAlgo.allocateElev(building_file, calls_file, 'out.csv')
        with open('out.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                if (row[5] == -1):
                    isRight = False
        self.assertTrue(isRight)

    def testAllocationWrong(self):
        # Writing a wrong CSV file (with a -1 in the allocation)
        calls_file = 'Ex1_input/Ex1_Calls/Calls_a.csv'
        building_file = 'Ex1_input/Ex1_Buildings/B5.json'
        b = Building.Building(building_file)
        numOfElev = b.numOfElevators
        f = open('wrongCSV.csv', 'a', newline='')
        for i in range(1, 101):
            tmpCall = Call.Call(calls_file, i)
            writer = csv.writer(f)
            if (i != 5):
                row = ['Elevator call', tmpCall.time, tmpCall.src, tmpCall.dest, 0, random.randint(0, numOfElev - 1)]
            else:
                row = ['Elevator call', tmpCall.time, tmpCall.src, tmpCall.dest, 0, -1]
            writer.writerow(row)
        f.close()
        # check this wrong file
        isRight = True
        with open('wrongCSV.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                if (int(row[5]) == -1):
                    isRight = False
        self.assertFalse(isRight)