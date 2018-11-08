import hmac
import hashlib
import base64

import aiohttp
import logging

logger = logging.getLogger(__name__)

from . import config

def authenticate_request(request: aiohttp.web.Request, body: bytes):
    try:
        client_name = request.match_info['client_name']
    except KeyError:
        logger.error("Request without client_name, ensure request is on the form /client_name")
        return False

    client_token = config.client_auth.get(client_name)

    if not client_token:
        logger.error(f"client_name {client_name} not found in configuration")
        return False

    (protocol, authdigest) = request.headers['Authorization'].split(" ")

    if protocol != "HMAC":
        logger.error(f"Invalid Authorization header {request.headers['Authorization']}")
        return False

    authdigest = authdigest.encode('ascii')

    digest = hmac.new(base64.b64decode(client_token), body, digestmod=hashlib.sha256).digest()

    return base64.b64encode(digest) == authdigest








