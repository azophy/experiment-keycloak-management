from pprint import pprint
import generate as generate
import keycloak as keycloak

print('retrieving admin token')
keycloak.GLOBAL_TOKEN = keycloak.get_access_token()
print('token:', keycloak.GLOBAL_TOKEN)

print('before add')
# kalau pakai auth dengan service account, pastikan dulu role di web admin keycloak sudah di atur
# di poin 10 di https://www.keycloak.org/docs/latest/server_admin/index.html#_service_accounts tambahkan semua role yg tersedia utk client nya
print('user count:', keycloak.send_request(f'/admin/realms/{keycloak.KEYCLOAK_REALM}/users/count'))

new_users = [
    generate.generate_dummy_user_payload()
    for _ in range(10)
]

res = keycloak.send_request(f'/admin/realms/{keycloak.KEYCLOAK_REALM}/partialImport',
    method = 'POST',
    json_body = { 'users': new_users },
)

print('after add')
print('user count:', keycloak.send_request(f'/admin/realms/{keycloak.KEYCLOAK_REALM}/users/count'))

# result from this action is list of all username including its new id. we
# could store this new id to trigger sending password reset email later
user_id_mapping = {}
if res:
    print('adding users done')
    for item in res['results'] :
        user_id_mapping[item['resourceName']] = item['id']

    pprint(user_id_mapping)

print('sending reset password email for 1 user')
example_user_id = list(user_id_mapping.values())[0]
try:
    res = keycloak.send_request(f'/admin/realms/{keycloak.KEYCLOAK_REALM}/users/{example_user_id}/execute-actions-email?lifespan=3600',
        method = 'PUT',
        json_body = [ 'UPDATE_PASSWORD' ],
    )
except Exception as e:
    print('encounter error:', e)
else:
    print(res)

print('==============================================')
print('get resourceId of our client')
res = keycloak.send_request(f'/admin/realms/{keycloak.KEYCLOAK_REALM}/clients?clientId={keycloak.KEYCLOAK_CLIENT_ID}')
CLIENT_RESOURCE_ID=res[0]['id']
print('==============================================')
print('setting up redirect url for our existing client')
res = keycloak.send_request(f'/admin/realms/{keycloak.KEYCLOAK_REALM}/clients/{CLIENT_RESOURCE_ID}',
    method = 'PUT',
    json_body = {
        'baseUrl': keycloak.KEYCLOAK_BASE_URL,
        'redirectUris': [
            '*'
        ],
    },
)

"""
print('==============================================')
print('create new OIDC client with attribute mapper for access token')
res = keycloak.send_request(f'/admin/realms/{keycloak.KEYCLOAK_REALM}/clients',
    method = 'POST',
    json_body = {
        'clientId': 'test_client_4',
        'name': 'test_client',
        'access': {
            'view': True,
            'configure': True,
            'manage': True
        },
        'enabled': True,

        'protocol': 'openid-connect',
        'publicClient': True,
        'directAccessGrantsEnabled': False,
        'standardFlowEnabled': True,
        'implicitFlowEnabled': False,
        'fullScopeAllowed': True,
        'defaultClientScopes': [
            'web-origins',
            'role_list',
            'profile',
            'roles',
            'email'
        ],

        'baseUrl': keycloak.KEYCLOAK_BASE_URL,
        'redirectUris': [
            '*'
        ],

        # add NIK attribute to map in access token
        'protocolMappers': [
            {
                'protocol':'openid-connect',
                'config':{
                    'id.token.claim':'true',
                    'access.token.claim':'true',
                    'userinfo.token.claim':'true',
                    'multivalued':'',
                    'aggregate.attrs':'',
                    'user.attribute':'nik',
                    'claim.name':'nik',
                    'jsonType.label':'String'
                },
                'name':'nik',
                'protocolMapper':'oidc-usermodel-attribute-mapper',
            },
        ],
    },
)
if res:
    print('success:', res)

print('==============================================')
print('create new client with service account permission')
res = keycloak.send_request(f'/admin/realms/{keycloak.KEYCLOAK_REALM}/clients',
    method = 'POST',
    json_body = {
        'clientId': 'backend_server3',
        'name': 'backend_server',
        'access': {
            'view': True,
            'configure': True,
            'manage': True
        },
        'enabled': True,

        'protocol': 'openid-connect',
        'publicClient': False,
        'serviceAccountsEnabled': True,
        'directAccessGrantsEnabled': False,
        'standardFlowEnabled': False,
        'implicitFlowEnabled': False,
        'fullScopeAllowed': True,
        'defaultClientScopes': [
            'web-origins',
            'role_list',
            'profile',
            'roles',
            'email'
        ],

        'baseUrl': keycloak.KEYCLOAK_BASE_URL,
        'redirectUris': [
            '*'
        ],
    },
)
if res:
    print('success:', res)
"""
