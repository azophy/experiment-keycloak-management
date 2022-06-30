import uuid
from faker import Faker

fake = Faker()

def generate_dummy_user_payload():
    profile = fake.profile()

    return {
      'id': str(uuid.uuid1()),
      'username' : profile['username'],
      'firstName': profile['name'].split()[0],
      'lastName' : profile['name'].split()[1],
      'email'    : profile['mail'],
      'attributes':{
        'nik':[ fake.numerify('#'*16) ]
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
    }

if __name__ == '__main__' :
    print(generate_dummy_user_payload())
