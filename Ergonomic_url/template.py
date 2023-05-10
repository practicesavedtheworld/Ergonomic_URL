import aiohttp.web
import jinja2
import aiohttp_jinja2
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.parent / 'templates'


def setup_jinja(app: aiohttp.web.Application):
    loader = jinja2.FileSystemLoader(str(PROJECT_ROOT))
    j_env = aiohttp_jinja2.setup(app=app, loader=loader)
    return j_env
