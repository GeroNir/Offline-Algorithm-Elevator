import json
from types import SimpleNamespace

with open ('Ex1_Buildings/B2.json') as b1:
    data = json.load(b1)

# Parse JSON into an object with attributes corresponding to dict keys.
x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
print(x._minFloor)