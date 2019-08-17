import json, datetime, sys

home = sys.argv[1]

def correcttime(tmp):
    if 'time' in tmp:
        tmp['time'] = tmp['time'][0:2] + ":" + tmp['time'][2:]
    return tmp


def parse(data):
    clock = datetime.datetime.now()
    time = ("0" if (clock.hour+2) < 10 else "") + str(clock.hour+2) + ("0" if (clock.minute) < 10 else "") + str(clock.minute)
    time = str(int(time)+5)
    time = ("0" if len(time) == 3 else "") + time
    now = None
    nowtmp = {
      "text" : "Closed"
    }
    upcomming = None
    upcommingtmp = {
      "time" : "Closed",
      "text" : "Closed"
    }
    for e in data['events']:
        if int(e['time']) <= int(time):
            if now is None or int(e['time']) > int(now):
                now = e['time']
                nowtmp = e
        if int(e['time']) > int(time):
            if upcomming is None or int(e['time']) < int(upcomming):
                upcomming = e['time']
                upcommingtmp = e
    return {
        "now" : correcttime(nowtmp),
        "upcomming" : correcttime(upcommingtmp)
    }


current_json = []

with open(home + '/public_html/base.json') as base_json:
    with open(home + '/public_html/saturday.json') as today_json:
        base_json = json.load(base_json)
        today_json = json.load(today_json)
        for b in base_json:
            tmp = b.copy()
            name = b['id']
            current = parse(today_json[name])
            tmp.update(current)
            current_json.append(tmp)

with open(home + '/public_html/current.json', 'w') as outfile:
    json.dump(current_json, outfile)
