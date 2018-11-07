import ssl
import asyncio
import logging
from aiohttp_negotiate import NegotiateClientSession

class TargetProcessClient(object):
    def __init__(self, url, cafile="/usr/local/etc/local-ca-certificates/all.crt"):
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
                                      params={'where':f"Id eq {tp_id}"},
                                      ssl_context=self.ssl_context) as response:
            return await response.text()


async def main():
    tp = TargetProcessClient("https://tp.niradynamics.local")
    xml = await tp.get_assignable_by_id("38903")
    print(xml)
    await tp.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


