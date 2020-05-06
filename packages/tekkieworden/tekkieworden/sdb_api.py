import time
from dotenv import dotenv_values
import json
from rauth import OAuth2Service


class Studiekeuzedb_api():
    url = None
    client_id = None
    client_secret = None
    grant_type = None
    access_token = None
    access_token_expiration = None

    def __init__(self, access_token_url, client_id, client_secret):
        self.name = "studiekeuze123_api"
        self.BASE_URL = "https://api.studiekeuzedatabase.nl/Studiekeuzedatabase.svc"
        self.access_token_url = "https://token.studiekeuzedatabase.nl/token"
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = 'client_credentials'

        try:
            self.service = OAuth2Service(
                name = self.name,
                client_id=self.client_id,
                client_secret=self.client_secret,
                access_token_url=self.access_token_url,
                authorize_url=self.access_token_url,
                base_url=self.BASE_URL,
            )

            self.access_token = self.getAccessToken()
            if self.access_token is None:
                raise Exception("Request for access token failed")
        except Exception as e:
            print(e)
        else:
            self.access_token_expiration = time.time() + 3500

    def getClientID(self):
        client_id = dotenv_values()['CLIENT_ID']
        return client_id

    def getClientSecret(self):
        client_secret = dotenv_values()['CLIENT_SECRET']
        return client_secret

    def getAccessToken(self):
        try:
            data = {'grant_type': self.grant_type,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret}
            token = self.service.get_access_token(data=data, decoder=json.loads)

        except Exception as e:
            print (e)
            return None
        else:
            return token

    def getSession(self, token):
        try:
            session = self.service.get_session(token=token)
        except Exception as e:
            print(e)
            return None
        else:
            return session

    class Decorators():
        @staticmethod
        def refreshToken(decorated):
            def wrapper(api, *args, **kwargs):
                if time.time() > api.access_token_expiration:
                    api.getAccessToken()
                return decorated(api, *args, **kwargs)

            return wrapper


    @Decorators.refreshToken
    def someRequest():
        # make our API request
        pass