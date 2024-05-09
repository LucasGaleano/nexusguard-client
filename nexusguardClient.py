
import requests
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class nexusguardClient():
    
    appID: str
    appSecret: str
    urlOauth: str = "https://api.nexusguard.com/oauth/credit/token"
    urlAPI:str = 'https://api.nexusguard.com/api'
    token: str = ''
    tokenExpires: datetime = field(init=False)

    def connect(self):
        data = {'app_id':self.appID, 'secret':self.appSecret, 'grant_type':'client_credential'}
        response = requests.post(self.urlOauth, data=data)
        codeStatus = response.json()['code']
        if codeStatus != 0:
            raise Exception(response.json()['msg'])
        result = response.json()['result']

        self.token = result['access_token']
        self.tokenExpires = datetime.now() + timedelta(seconds=int(result['expires_in']))
        print('token generated')

    def renew_token(self):
        if datetime.now() > self.tokenExpires:
            self.connect()
            print('token renewed')

    def make_request(self, endpoint, extraData=None):
        if not extraData:
            extraData = {}

        self.renew_token()
        data = {'access_token':self.token} | extraData
        url = self.urlAPI + endpoint
        return requests.get(url, data).json()['result']
        
    def get_alerts(self, siteID, numLastAlerts:int=10):
        extraData = {'num':numLastAlerts}
        return self.make_request(f'/specp/op/dashboard/site/{siteID}/ddos_events', extraData)

    def get_last_alert(self, siteID):
        return self.get_alerts(siteID, 1)
    
    def get_alert_detail(self, siteID, alertID):
        return self.make_request(f'/specp/op/dashboard/site/{siteID}/ddos_event/{alertID}')

    def get_sites(self):
        return self.make_request(f'/specp/op/sites')
    
    def is_finished(self, status):
        return not int(status)
        



