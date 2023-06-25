from django.contrib.auth import authenticate
import json
import requests
import jwt
from jwt.algorithms import RSAAlgorithm


def jwt_get_username_from_payload_handler(payload):
    identifier = payload.get('sub')
    authenticate(remote_user=identifier)
    return identifier


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format('dev-gybtlqrqithbjmgz.us.auth0.com')).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format('dev-gybtlqrqithbjmgz.us.auth0.com')
    try:
        jwt_result = jwt.decode(token, public_key, audience='YpRo7KJC5yLf3K18bBRk7cyNo5zvqDMC', issuer=issuer, algorithms=['RS256'])
        return jwt_result
    except Exception as e:
        print(str(e))
