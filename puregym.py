import requests

email = ''
pin = ''

class PuregymAPIClient():
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'PureGym/1523 CFNetwork/1312 Darwin/21.0.0'}
    authed = False
    home_gym_id = None
    
    def login(self, email, pin):
        self.session = requests.session()
        data = {
            'grant_type': 'password',
            'username': email,
            'password': pin,
            'scope': 'pgcapi',
            'client_id': 'ro.client'
        }
        response = self.session.post('https://auth.puregym.com/connect/token', headers=self.headers, data=data)
        if response.status_code == 200:
            self.auth_json = response.json()
            self.authed = True
            self.headers['Authorization'] = 'Bearer '+self.auth_json['access_token']
        else:
            return response.raise_for_status()
    
    def get_home_gym(self):
        if not self.authed:
            return PermissionError('Not authed: call login(email, pin)')

        response = self.session.get('https://capi.puregym.com/api/v1/member', headers=self.headers)
        if response.status_code == 200:
            self.home_gym_id = response.json()['homeGymId']
        else:
            return ValueError('Response '+str(response.status_code))
    
    def get_gym_attendance(self):
        if not self.authed:
            return PermissionError('Not authed: call login(email, pin)')
        if self.home_gym_id == None:
            self.get_home_gym()
        
        response = self.session.get(f'https://capi.puregym.com/api/v1/gyms/{str(self.home_gym_id)}/attendance', headers=self.headers)
        if response.status_code == 200:
            return response.json()['totalPeopleInGym']
        else:
            return response.raise_for_status()

client = PuregymAPIClient()
client.login(email, pin)
client.get_home_gym()
print(client.get_gym_attendance())