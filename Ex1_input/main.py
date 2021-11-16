import json
#
# file = open('Ex1_Buildings/B1.json', 'r')
# print(file.readlines())


b1 = '''
{
  "_minFloor": -2,
  "_maxFloor": 10,
  "_elevators": [
    {
      "_id": 0,
      "_speed": 0.5,
      "_minFloor": -2,
      "_maxFloor": 10,
      "_closeTime": 2.0,
      "_openTime": 2.0,
      "_startTime": 3.0,
      "_stopTime": 3.0
    }
  ]
}
 '''
data = json.loads(b1)
new_string = json.dumps(data, indent=2, sort_keys=True)
print(data['_elevators'][0]['_id'])
# print(new_string)

with open ('Ex1_Buildings/B2.json') as b1:
    data = json.load(b1)

# with open('myJson.json', 'w') as b1:
#     json.dump(data, b1, indent=2)