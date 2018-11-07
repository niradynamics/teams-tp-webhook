import re
import aiohttp
import datetime
import json

from botbuilder.schema import Activity

from .targetprocess import TargetProcessClient

tp = TargetProcessClient("https://tp.niradynamics.local")

async def index(request: aiohttp.web.Request):
    headers = request.headers
    jsondata = await request.content.read()

    data = json.loads(jsondata)

    activity = Activity.deserialize(data)

    mo = re.search("#(?P<id>[0-9]+)", activity.text)

    if mo:
        tpdata = await tp.get_assignable_by_id(mo.group("id"))
    else:
        tpdata = "Sorry, please format TP issues as #99999"

    return aiohttp.web.json_response(
        {
            "type":"message",
            "text":tpdata
         }
    )