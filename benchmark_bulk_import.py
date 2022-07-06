from pprint import pprint
from datetime import datetime
import generate as generate
import keycloak as keycloak

NUM_USER_GENERATED = 1000
NUM_ATTEMPT = 10
print('NUM_USER_GENERATED:', NUM_USER_GENERATED)

print('retrieving admin token')
keycloak.GLOBAL_TOKEN = keycloak.get_access_token()
print('token:', keycloak.GLOBAL_TOKEN)

def execute_benchmark():
    before_count=keycloak.send_request(f'/admin/realms/{keycloak.KEYCLOAK_REALM}/users/count')

    username_prefix = str(datetime.now().timestamp()).replace('.', '')
    print('username_prefix:', username_prefix)

    new_users = [
        generate.generate_dummy_user_payload(username_prefix + str(i))
        for i in range(NUM_USER_GENERATED)
    ]

    before_time = datetime.now()
    try:
        res = keycloak.send_request(f'/admin/realms/{keycloak.KEYCLOAK_REALM}/partialImport',
            method = 'POST',
            json_body = { 'users': new_users },
        )
    except Exception as e:
        print('encounter error:', e)
    after_time = datetime.now()

    after_count=keycloak.send_request(f'/admin/realms/{keycloak.KEYCLOAK_REALM}/users/count')

    time_diff = after_time - before_time
    count_diff = after_count - before_count

    return (time_diff, count_diff)

if __name__ == '__main__':
    valid_time_diffs = []
    for attempt in range(NUM_ATTEMPT):
        (time_diff, count_diff) = execute_benchmark()
        print('attempt #', attempt+1,
              'count diff:', count_diff,
              'time_diff:', time_diff.total_seconds()
        )

        if count_diff > 0:
            valid_time_diffs.append(time_diff.total_seconds())

    print('num valid diff:', len(valid_time_diffs))
    print('avg of valid diff:', sum(valid_time_diffs)/len(valid_time_diffs))
