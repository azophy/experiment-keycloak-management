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
res = keycloak.send_request(f'/admin/realms/{keycloak.KEYCLOAK_REALM}/users/{example_user_id}/execute-actions-email?lifespan=3600',
    method = 'PUT',
    json_body = [ 'UPDATE_PASSWORD' ],
)

print(res)

