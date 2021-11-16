import sys
import OfflineAlgo

# This program let run the algorithm from the command line
if __name__ == "__main__":
    building = sys.argv[1]
    csv_calls = sys.argv[2]
    csv_out = sys.argv[3]
    OfflineAlgo.allocateElev(building, csv_calls, csv_out)