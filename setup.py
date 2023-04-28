import requests
from pprint import pprint
import yaml
from yaml.loader import SafeLoader

with open('config.yml') as f:
    data = yaml.load(f, SafeLoader)
    
class RestSetup:

    def __init__(self):
        self.CLIENT_ID = data['CLIENT_ID']
        self.__CLIENT_SECRET = data['CLIENT_SECRET']
        self.__AUTH_URL = 'https://accounts.spotify.com/api/token'
        self.__access_token = ''
        self.__headers = ''
    
        # POST
        auth_response = requests.post(self.__AUTH_URL, {
            'grant_type' : 'client_credentials',
            'client_id': self.CLIENT_ID,
            'client_secret': self.__CLIENT_SECRET,
        })

        # convert the response to JSON
        auth_response_data = auth_response.json()

        # save the access token
        self.__access_token = auth_response_data['access_token']
    
        # set up header
        self.__headers = {
            'Authorization': f'Bearer {self.__access_token}'
        }

    def get_headers(self):
        return self.__headers