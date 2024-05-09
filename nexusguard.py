from nexusguardClient import nexusguardClient
import configparser
import time
import json


config = configparser.ConfigParser()
config.read('nexusguard.conf')

n = nexusguardClient(appID=config['nexus']['appID'], appSecret=config['nexus']['appSecret'])

try:
    n.connect()
except Exception as e:
    print(e)
    exit()


siteID = config['nexus']['siteID']
ongoingAlerts = dict()

while True:

    alerts = n.get_alerts(siteID)['result']
    for alert in alerts['events']:
        # if lastAlert == alert['alert_id']:
        #     break
        if n.is_finished(alert['status']):
            continue 
        alert['app'] = 'nexusguard'
        print(json.dumps(alert))

    lastAlert = alerts['events'][0]['alert_id']

    time.sleep(60)

"""
{
  "code": 0,
  "msg": "Success.",
  "result": {
    "total": 38,
    "events": [
      {
        "severity": 3,
        "attack_type": "Abnormal",
        "end_time": 1715145300,
        "severity_level": "Auto Mitigation",
        "profile_desc": "AS9999",
        "max_pps": 275165,
        "duration": 721,
        "site_name": "company_name",
        "start_time": 1715144580,
        "profile_name": "AS111111",
        "site_ip": "134.44.233.32",
        "alert_id": "EVENT-123456789ABDCDEF",
        "p_type": 1,
        "status": 0,
        "max_bps": 1308675998
      },
"""