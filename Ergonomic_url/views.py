import aiohttp.web
import aiohttp_jinja2
from aiohttp.web_request import Request
from aiohttp.web_response import Response


@aiohttp_jinja2.template('index.html')
async def index(request: Request) -> Response:
    pass