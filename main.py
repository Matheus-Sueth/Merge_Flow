import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

class Genesys:
    URL_AUTH = os.environ.get('URL_AUTH')
    URL = os.environ.get('URL')
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

    def __init__(self) -> None:
        self.token = self.get_token()
        self.verificar_token()

    def __new__(self, *args):
        if not hasattr(self, 'instance'):
            self.instance = super(Genesys, self).__new__(self)
        return self.instance

    def get_token(self) -> str:
        authorization = base64.b64encode(bytes(self.CLIENT_ID + ":" + self.CLIENT_SECRET, "ISO-8859-1")).decode("ascii")

        request_headers = {
            "Authorization": f"Basic {authorization}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        request_body = {
            "grant_type": "client_credentials"
        }

        response = requests.post(f"https://login.{self.URL_AUTH}/oauth/token", data=request_body, headers=request_headers)

        if response.status_code == 200:
            response_json = response.json()
            return response_json['access_token']
        else:
            raise Exception(f"Failure: {response.status_code} - {response.reason}")
    
    def verificar_token(self) -> None:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"bearer {self.token}"
        }
        response = requests.head(url='https://'+self.URL+'/api/v2/tokens/me', headers=headers)
        if response.status_code != 200:
            raise Exception(f'Token Genesys inválido, failure: {response.status_code} - {response.reason}')
        return None
    
api = Genesys()