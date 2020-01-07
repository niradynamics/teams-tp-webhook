import argparse
from aiohttp import web
from . import config


def configure_app():
    # Import here so any configuration override has been added.
    from .handler import handle_mention

    app = web.Application()
    app.add_routes([web.post("/{client_name}", handle_mention)])
    return app

def main():
    parser = argparse.ArgumentParser(description="Teams TP Webhook server")
    parser.add_argument("--port", type=int)
    parser.add_argument("--config-file", "-c")

    args = parser.parse_args()
    config.add_override(args.config_file)

    app = configure_app()

    web.run_app(app, reuse_port=True, reuse_address=True, port=args.port)
