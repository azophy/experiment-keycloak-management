import base64
import os

import requests
from dotenv import load_dotenv
load_dotenv()

GLOBAL_TOKEN = None
KEYCLOAK_BASE_URL = os.getenv('KEYCLOAK_BASE_URL')
KEYCLOAK_ADMIN_USERNAME = os.getenv('KEYCLOAK_ADMIN_USERNAME')
KEYCLOAK_ADMIN_PASSWORD = os.getenv('KEYCLOAK_ADMIN_PASSWORD')
KEYCLOAK_REALM = os.getenv('KEYCLOAK_REALM')
KEYCLOAK_CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID')
KEYCLOAK_CLIENT_SECRET = os.getenv('KEYCLOAK_CLIENT_SECRET')

def get_access_token():
    """
    # using access acocount
    response = requests.request(
            method = 'POST',
            url = KEYCLOAK_BASE_URL +
                  # path yg benar utk keycloak versi saat ini depannya tidak pakai `/auth`. ref: https://www.keycloak.org/docs/latest/securing_apps/index.html#token-endpoint
                  f'/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token',
            data = {
                'grant_type'    : 'client_credentials',
                'client_id'     : KEYCLOAK_CLIENT_ID,
                'client_secret' : KEYCLOAK_CLIENT_SECRET,
            },
    )
    """
    # without access account
    response = requests.request(
            method = 'POST',
            url = KEYCLOAK_BASE_URL +
                  "/realms/master/protocol/openid-connect/token",
            data = {
                'client_id': 'admin-cli',
                'username': KEYCLOAK_ADMIN_USERNAME,
                'password': KEYCLOAK_ADMIN_PASSWORD,
                'grant_type': 'password',
            },
    )
    if not response:
        raise Exception(f'response code {response.status_code}')

    return response.json()['access_token']

def send_request(path, method='GET', json_body=[], token=None):
    token = token if token is not None else GLOBAL_TOKEN
    url = KEYCLOAK_BASE_URL + path

    response = requests.request(
            method = method,
            url = url,
            json = json_body,
            headers = {
                'Authorization': 'Bearer ' + token
            }
    )

    if not response:
        print(response.content)
        raise Exception(f'response code {response.status_code} from {method}  {url}')

    if 'Content-Type' in response.headers and \
    'json' in response.headers['Content-Type'] :
        return response.json()
    else:
        return response.text

