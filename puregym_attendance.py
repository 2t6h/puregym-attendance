import requests
import textdistance


class PuregymAPIClient():
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'PureGym/1523 CFNetwork/1312 Darwin/21.0.0'}
    home_gym_id = None
    gyms = None
    
    def __init__(self, email, pin):
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
            self.headers['Authorization'] = 'Bearer ' + response.json()['access_token']
        else:
            return response.raise_for_status()
    
    def get_list_of_gyms(self):
        response = self.session.get(f'https://capi.puregym.com/api/v2/gyms/', headers=self.headers)
        if response.status_code == 200:
            self.gyms = {i['Name'].replace(' ', '').replace('-', '').lower(): i['Id'] for i in response.json()}
        else:
            return ValueError('Response '+str(response.status_code))
    
    def get_gym(self, gym_name):
        """returns corrected gym name and its ID"""
        gym_name = gym_name.replace(' ', '').replace('-', '').lower()
        if self.gyms is None:
            self.get_list_of_gyms()
        return max(list(self.gyms.items()), key=lambda x: textdistance.levenshtein.similarity(gym_name, x[0]))

    def get_home_gym(self):
        response = self.session.get('https://capi.puregym.com/api/v2/member', headers=self.headers)
        if response.status_code == 200:
            home_gym = response.json()['HomeGym']
            self.home_gym_id = home_gym['Id']
            return home_gym
        else:
            return ValueError('Response '+str(response.status_code))
    
    def get_gym_attendance(self, gym=None):
        if gym is None:
            if self.home_gym_id is None:
                self.get_home_gym()
            gym_id = self.home_gym_id
        elif isinstance(gym, int):
            gym_id = gym
        else:
            gym, gym_id = self.get_gym(gym)  # name->id
        response = self.session.get(f'https://capi.puregym.com/api/v2/gymSessions/gym?gymId={gym_id}', headers=self.headers)
        if response.status_code == 200:
            n = response.json()['TotalPeopleInGym']
            return n
        else:
            return response.raise_for_status()

    def get_member_activity(self):
        response = self.session.get("https://capi.puregym.com/api/v2/gymSessions/member", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return ValueError("Response " + str(response.status_code))


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('email')
    parser.add_argument('pin')
    parser.add_argument('--gym', default=None)
    args = parser.parse_args()

    client = PuregymAPIClient(
        email=args.email,
        pin=args.pin
    )
    print(f"Current attendance: {client.get_gym_attendance(args.gym)}")
    print(client.get_member_activity())
