EXPERIMENT WITH KEYCLOAK MANAGEMENT VIA REST API
================================================

## Items
- [x] retrieving admin access token
- [x] listing & counting users via `/users` endpoint
- [x] adding new users via `partialImport` endpoint
- [x] sending reset password link via email
- [x] setting redirect url dari client
- [x] setting mapping atribute nik sudah muncul di access token hasil login

## Requirement
- docker
- python > 3.6 with pip installed

## Usage
### Basic setup
- clone this repo
- cd to the folder
- edit .env.example into .env

### Setup python
- `pip instal -r requirements.txt`
- `python main.py`

### Setup keycloak (via docker)
- `docker compose up`
- from other terminal: `docker compose exec keycloak sh /app/keycloak-autosetup-script.sh`

## Used libraries
- faker
- requests
- python-dotenv
