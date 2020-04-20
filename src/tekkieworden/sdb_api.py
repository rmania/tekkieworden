"""
https://api.studiekeuzedatabase.nl/Studiekeuzedatabase.svc/
"""

import requests
from typing import Dict

class SDB:
    def __init__(self, token: str):
        self.__token = token
        self.__base_url = "https://api.studiekeuzedatabase.nl/"

    def __make_request(selfself, url: str, params: Dict = None, method ="GET"):

        response = requests.request(method, url, params=params)
        response.raise_for_status()

        return response.json()