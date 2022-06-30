# keycloak-autosetup-example.sh
# Adapted from : https://keycloak.ch/keycloak-tutorials/tutorial-1-installing-and-running-keycloak/

# basic variables. edit as needed
KCADM="/opt/keycloak/bin/kcadm.sh"
REALM_NAME=test_realm
CLIENT_ID=test_client
CLIENT_NAME="Test Client"
USER_NAME=testuser
USER_PASSWORD=testpassword

# establish connection session to keycloak
$KCADM config credentials --server http://localhost:8080 \
--user admin \
--password admin \
--realm master

# test connection
$KCADM get serverinfo

# setup new realm
$KCADM create realms -s realm="${REALM_NAME}" -s enabled=true

# setup client
$KCADM create clients -r ${REALM_NAME} \
-s clientId="${CLIENT_ID}" \
-s enabled=true \
-s name="${CLIENT_NAME}" \
-s protocol=openid-connect \
-s publicClient=true \
-s standardFlowEnabled=true \
-s 'redirectUris=["https://www.keycloak.org/app/*"]' \
-s baseUrl="https://www.keycloak.org/app/" \
-s 'webOrigins=["*"]'

# setup user
$KCADM create users -r $REALM_NAME \
-s username="${USER_NAME}" \
-s enabled=true \
-s firstName="My" \
-s lastName="User" \
-s email="my.user@example.com"
## setup user password
$KCADM set-password -r $REALM_NAME \
--username "${USER_NAME}" \
--new-password "${USER_PASSWORD}"

