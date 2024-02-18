from pprint import pprint
import json
import datetime
import time

from startgg import request

def yearToTimeStamp(year):
    date_time = datetime.datetime(year, 1, 1, 0, 0)
    return int(time.mktime(date_time.timetuple()))

# data = request("query_tournaments.gql", {"$page": "0", "$afterDate": yearToTimeStamp(2019), "$beforeDate": yearToTimeStamp(2020)})
# pprint(data)


for year in range(2018, 2024):
    events = []
    page = 1
    totalPages = 9999
    while True:
        data = request("query_tournaments.gql", {"$page": "0", "$afterDate": yearToTimeStamp(year), "$beforeDate": yearToTimeStamp(year+1)})

        for n in data["tournaments"]["nodes"]:
            events.extend(n["events"])
        
        totalPages = data["tournaments"]["pageInfo"]["totalPages"]
        print(f"{year}: {page}/{totalPages}")
        if page >= totalPages:
            break
        page += 1

    events = [e for e in events if e["videogame"]["id"] == 1386 and not e["isOnline"]]
    events.sort(key=lambda l: l["startAt"])
    json.dump(events, open(f"events/events_{year}.json", "w"))