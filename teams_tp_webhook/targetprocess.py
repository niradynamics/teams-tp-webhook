import ssl
import asyncio
import logging
from aiohttp_negotiate import NegotiateClientSession
from . import config

class TargetProcessClient(object):
    def __init__(self, url, cafile=config.cafile):
        self._url = url
        self._session = None
        self._cafile = cafile
        self._ssl_context = None

    @property
    def session(self):
        if self._session is None:
            self._session = NegotiateClientSession()
        return self._session

    @property
    def ssl_context(self):
        if self._ssl_context is None:
            self._ssl_context = ssl.create_default_context(cafile=self._cafile)
        return self._ssl_context

    async def get_assignable_by_id(self, tp_id: str):
        async with self.session.get(f"{self._url}/api/v1/Assignables/",
                                      params={'where':f"Id eq {tp_id}",
                                              'include':'[Name]',
                                              'format':'json'},
                                      ssl_context=self.ssl_context) as response:
            return await response.json()


async def main(tp_id):
    tp = TargetProcessClient(config.tp_url)
    data = await tp.get_assignable_by_id(tp_id)
    print(data)
    if data:
        print (data['Items'][0]['Name'])
    await tp.session.close()

def cmdline():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", "-c")
    parser.add_argument("--verbose", "-v", action='store_true', default=False)
    parser.add_argument("tp_id")

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    config.add_override(args.config_file)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.tp_id))


