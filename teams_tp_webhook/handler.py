import re
import aiohttp
import datetime
import json
import hmac
import hashlib
import base64

from botbuilder.core import CardFactory
from botbuilder.schema import Activity, HeroCard
from botbuilder.schema.connector_client_enums import AttachmentLayoutTypes

from . import config
from .auth import authenticate_request
from .targetprocess import TargetProcessClient

tp = TargetProcessClient(config.tp_url, access_token=config.tp_access_token)

async def handle_mention(request: aiohttp.web.Request):
    body = await request.read()

    if not authenticate_request(request, body):
        return aiohttp.web.Response(text="Unauthenticated", status=401)

    data = json.loads(body)

    activity = Activity.deserialize(data)

    response_activity = Activity()
    response_activity.text = ""
    mo = re.findall("(#|TP)(?P<id>[0-9]+)", activity.text)

    if mo:
        for tp_id in mo:
            resp = await tp.get_assignable_by_id(tp_id[1])
            items = resp['Items']
            if items:
                response_activity.text = f"""{response_activity.text}<h1>{tp_id[1]} - {items[0]['Name']}</h1><br/>
                <a href="https://tp.niradynamics.local/entity/{tp_id[1]}">view in TP</a><br/>
                """
            else:
                response_activity.text = f"{response_activity.text}No such TP item #<b>{tp_id[1]}</b><br/>"
    else:
        response_activity.text = "Sorry, I don't understand. Please include a TP issue formatted as <b>#99999</b>"

    print (response_activity.as_dict())


    return aiohttp.web.json_response(
        response_activity.as_dict()
    )