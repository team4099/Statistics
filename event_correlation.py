import requests
from statistics import mean
from json import loads

headers = {
    "X-TBA-App-Id": "frc4099:statistics:0.0.1"
}

URL = "https://www.thebluealliance.com/api/v2/"

event_hits = {}
for i in range(14):
    page = requests.get(URL + "teams/" + str(i), headers=headers)
    info = loads(page.text)
    for team_info in info:
        while True:
            try:
                key = team_info["key"]
                page = requests.get(URL + "team/" + key + "/2017/events", headers=headers)
                info = loads(page.text)

                events = 0
                worlds = False
                for event in info:
                    event_type = event["event_type_string"].casefold()
                    events += "championship" not in event_type and "offseason" not in event_type
                    if event_type.startswith("championship"):
                        worlds = True

                if events not in event_hits:
                    event_hits[events] = []

                event_hits[events].append(worlds)
                break
            except:
                pass

averages = event_hits.copy()
for key in averages:
    averages[key] = mean(map(int, averages[key]))

print(averages)
