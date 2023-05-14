import asyncio
import aiohttp.web

from settings import load_config
from template import setup_jinja
from routes import setup_routes
from init_db import connect_to_db
from middlewares import link_middleware

def start_app() -> None:
    app = aiohttp.web.Application()
    app['config'] = load_config()
    setup_jinja(app=app)
    setup_routes(app=app)
    app.middlewares.append(link_middleware)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_to_db(app))
    aiohttp.web.run_app(app, loop=loop)


if __name__ == '__main__':
    start_app()
