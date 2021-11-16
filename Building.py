import json


class Building:

    minFloor = 0
    maxFloor = 0
    Elevators = ['']
    numOfElevators = 0

    # This constructor read from the json file the relevant details
    def __init__(self, file):
        with open(file) as b1:
            data = json.load(b1)
        self.minFloor = data['_minFloor']
        self.maxFloor = data['_maxFloor']
        self.Elevators = data['_elevators']
        self.numOfElevators = len(data['_elevators'])
