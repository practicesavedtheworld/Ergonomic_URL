import aiohttp.web
import aiohttp_jinja2
from aiohttp.web_request import Request


@aiohttp_jinja2.template('index.html')
async def index(request: Request):
    return {'name': 'Ergonomic your URL'}
