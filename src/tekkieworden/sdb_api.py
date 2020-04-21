"""
https://api.studiekeuzedatabase.nl/Studiekeuzedatabase.svc/
"""
from rauth import OAuth2Service
import requests
from typing import Dict

from dotenv import dotenv_values


class ExampleOAuth2Client:
    def __init__(self, client_id, client_secret):
        self.access_token = None

        self.service = OAuth2Service(
            name="studiekeuze_api",
            client_id=dotenv_values()['CLIENT_ID'],
            client_secret=dotenv_values()['CLIENT_SECRET'],
            access_token_url="https://token.studiekeuzedatabase.nl/token",
            authorize_url="https://token.studiekeuzedatabase.nl/token",
            base_url="https://api.studiekeuzedatabase.nl/Studiekeuzedatabase.svc/",
        )

        self.get_access_token()

    def get_access_token(self):
        data = {'code': 'bar',
                'grant_type': 'client_credentials',
                'redirect_uri': 'http://example.com/'}

        session = self.service.get_auth_session(data=data, decoder=json.loads)

        self.access_token = session.access_token


class SDB:
    def __init__(self, token: str):
        self.__token = token
        self.__base_url = "https://api.studiekeuzedatabase.nl/"

    def __make_request(selfself, url: str, params: Dict = None, method ="GET"):

        response = requests.request(method, url, params=params)
        response.raise_for_status()

        return response.json()