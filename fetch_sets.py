from pprint import pprint
import json
import glob
import os
import datetime
import logging

from startgg import request
events_files = glob.glob("events/*.json")

# data = request("query_sets.gql", {"$page": "0", "$id": "278612"})
# pprint(data)

events = []

for events_file in events_files:
    events.extend(json.load(open(events_file, "r")))

for i, event in enumerate(events):
    filename = f"sets/sets_{event['id']}.json"

    progress = f"{datetime.datetime.now()} {event['id']} ({i}/{len(events)})"

    if os.path.exists(filename):
        print(f"{progress}: skipped")
        continue

    sets = []
    page, totalPages = 1, 9999
    while True:
        data = request("query_sets.gql", {"$page": "0", "$id": event["id"]})
        sets.extend(data["event"]["sets"]["nodes"])
        totalPages = data["event"]["sets"]["pageInfo"]["totalPages"]
        print(f"{progress}: {page}/{totalPages}")
        if page >= totalPages:
            break
        page += 1

    json.dump(sets, open(filename, "w"))