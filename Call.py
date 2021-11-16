import csv

time = 0
src = 0
dest = 0
numOfCalls = 0
status = 0
waitingTime = 0
id = 0

class Call:

    # This constructor read from the csv file the relevant details by his number
    def __init__(self, file, callNumber):
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 1
            for row in csv_reader:
                if line_count == callNumber:
                    self.time = row[1]
                    self.src = row[2]
                    self.dest = row[3]
                    line_count += 1
                else:
                    line_count += 1

        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row_count = sum(1 for row in csv_reader)
            self.numOfCalls = row_count
        if (src > dest):
            self.status = -1
        elif (dest > src):
            self.status = 1

        self.allocatedTo = 0
        self.id = callNumber