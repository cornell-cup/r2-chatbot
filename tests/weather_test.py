import json

with open("./city.list.min.json") as f:
    data = json.load(f)
    print(data)

