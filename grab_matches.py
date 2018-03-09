import requests, json, ast
import pprint
import time

pp = pprint.PrettyPrinter(indent=1)

def write_to_file():
    event_key = str(raw_input("Enter event key:"))
    matches=convert_unicode(requests.get("http://www.thebluealliance.com/api/v3/event/"+event_key+"/matches/simple", headers={"X-TBA-Auth-Key":"v62ZvFvAkyWVH1qwd1m8Kyyhll0VEvyxUGo7pqpM1re827yjVZlgtjdpBEQJNcn2"}).json())
    match_list_qm = {}
    for match in matches:
        if match.get('comp_level') == 'qm':
            match_qm = []
            ts = time.strftime('%I:%M%p', time.localtime(match.get('time'))).lstrip('0').lower()
            blue_teams = match.get('alliances').get('blue').get('team_keys')
            red_teams = match.get('alliances').get('red').get('team_keys')
            match_number = match.get('match_number')
            
            match_qm.extend((ts, blue_teams, red_teams))
            match_list_qm[match_number] = match_qm
            
    match_file = open(r"matches-azfl.txt","a")
    for key in sorted(match_list_qm.keys()):
        match = "%s %s" % (key, match_list_qm[key])
        match = match.translate(None, '[],\'frc') # get rid of certain characters
        match_file.write(match)
        match_file.write("\n")

    match_file.close()


def convert_unicode(input):
    if isinstance(input, dict):
        return {convert_unicode(key): convert_unicode(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert_unicode(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

write_to_file()
