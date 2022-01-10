import requests
import textdistance


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
    
    def get_list_of_gyms(self):
        if not self.authed:
            return PermissionError('Not authed: call login(email, pin)')
        response = self.session.get(f'https://capi.puregym.com/api/v1/gyms/', headers=self.headers)
        if response.status_code == 200:
            self.gyms = {i['name'].replace(' ', '').replace('-', '').lower(): i['id'] for i in response.json()}
        else:
            return ValueError('Response '+str(response.status_code))
    
    def get_gym(self, gym_name):
        """returns corrected gym name and its ID"""
        gym_name = gym_name.replace(' ', '').replace('-', '').lower()
        if self.gyms is None:
            self.get_list_of_gyms()
        return min(list(self.gyms.items()), key=lambda x: textdistance.levenshtein.distance(gym_name, x[0]))

    def get_home_gym(self):
        if not self.authed:
            return PermissionError('Not authed: call login(email, pin)')

        response = self.session.get('https://capi.puregym.com/api/v1/member', headers=self.headers)
        if response.status_code == 200:
            self.home_gym_id = response.json()['homeGymId']
        else:
            return ValueError('Response '+str(response.status_code))
    
    def get_gym_attendance(self, gym):
        if not self.authed:
            return PermissionError('Not authed: call login(email, pin)')
        if gym_id is None:
            if self.home_gym_id is None:
                self.get_home_gym()
            gym_id = self.home_gym_id
        else:
            gym, gym_id = self.get_gym(gym)  # name->id
        response = self.session.get(f'https://capi.puregym.com/api/v1/gyms/{gym_id}/attendance', headers=self.headers)
        if response.status_code == 200:
            return response.json()['totalPeopleInGym']
        else:
            return response.raise_for_status()

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('email')
    parser.add_argument('pin')
    parser.add_argument('--gym', default=None)
    args = parser.parse_args()
    
    client = PuregymAPIClient()
    client.login(args.email, args.pin)
    print(client.get_gym_attendance(args.gym))
