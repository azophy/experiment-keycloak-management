import base64
import os

import requests
from dotenv import load_dotenv
load_dotenv()

GLOBAL_TOKEN = None
KEYCLOAK_BASE_URL = os.getenv('KEYCLOAK_BASE_URL')
KEYCLOAK_REALM = os.getenv('KEYCLOAK_REALM')
KEYCLOAK_CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID'),
KEYCLOAK_CLIENT_SECRET = os.getenv('KEYCLOAK_CLIENT_SECRET'),

def get_access_token():
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

    return response.json()
    # return response.text

if __name__ == '__main__' :
    from pprint import pprint

    GLOBAL_TOKEN = get_access_token()
    print('token:', GLOBAL_TOKEN)

    print('before add')
    # pastikan dulu role di web admin keycloak sudah di atur
    # di poin 10 di https://www.keycloak.org/docs/latest/server_admin/index.html#_service_accounts tambahkan semua role yg tersedia utk client nya
    print(send_request(f'/admin/realms/{KEYCLOAK_REALM}/users/count'))

    from generate import *
    new_users = [
        generate_dummy_user_payload()
        for _ in range(10)
    ]

    res = send_request(f'/admin/realms/{KEYCLOAK_REALM}/users',
        method = 'POST',
        json_body = new_users,
    )

    print(res)

    print('after add')
    print(send_request(f'/admin/realms/{KEYCLOAK_REALM}/users/count'))

    # users = send_request(f'/admin/realms/{KEYCLOAK_REALM}/users')
    # pprint(users)
