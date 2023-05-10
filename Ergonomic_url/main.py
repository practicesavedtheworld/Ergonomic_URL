import aiohttp.web

from settings import load_config
from template import setup_jinja
from routes import setup_routes


def start_app() -> None:
    app = aiohttp.web.Application()
    app['config'] = load_config()
    setup_jinja(app=app)
    setup_routes(app=app)


    aiohttp.web.run_app(app)


if __name__ == '__main__':
    start_app()