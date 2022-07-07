import uuid
from faker import Faker

fake = Faker()

def generate_dummy_user_payload(username_prefix=''):
    # profile = fake.unique.profile()

    return {
      'id': str(uuid.uuid1()),
      'username' : username_prefix + fake.unique.user_name(),
      'firstName': fake.unique.first_name(),
      'lastName' : fake.unique.last_name(),
      'email'    : fake.unique.email(),
      'attributes':{
        'nik':[ fake.unique.numerify('#'*16) ]
      },
      # 'access':{
        # 'manageGroupMembership':true,
        # 'view':true,
        # 'mapRoles':true,
        # 'impersonate':true,
        # 'manage':true
      # },

      'disableableCredentialTypes':[],
      'requiredActions':[],
      'notBefore':0,
      'enabled':True,
      'totp':False,
      'emailVerified':True,

      # optional: creating password when creating user
      'credentials': [
          {
            'type': 'password',
            'value': 'test',
            'temporary': False,
          }
      ],
    }

def generate_multiple_dummy_user_payload(num, username_prefix=''):
    fake.unique.clear()

    return [
        generate_dummy_user_payload(username_prefix)
        for i in range(num)
    ]

if __name__ == '__main__' :
    # print(generate_dummy_user_payload())
    new_users = [
        generate_dummy_user_payload()
        for _ in range(10)
    ]

    # from pprint import pprint
    # pprint(new_users)
    import json
    print(json.dumps({ 'users': new_users }))
