import argparse
from aiohttp import web
from .handler import index

def configure_app():
    app = web.Application()
    app.add_routes([web.post('/', index)])
    return app

def main():
    parser = argparse.ArgumentParser(description="Teams TP Webhook server")
    parser.add_argument("--port", type=int)

    app = configure_app()

    args = parser.parse_args()
    web.run_app(app, reuse_port=True, reuse_address=True, port=args.port
    )

