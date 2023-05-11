import aiohttp_jinja2
import aiohttp.web
from aiohttp.web_request import Request

from utils import push_to_db, get_from_db


@aiohttp_jinja2.template('index.html')
async def index(request: Request):
    return {'name': 'Ergonomic your URL'}


async def ergonomic(request: Request):
    data = await request.json()
    original_link = data['url']
    short_link = await push_to_db(request.app, original_link)

    return aiohttp.web.json_response({'url': short_link})


async def redirect(request: Request):
    url = request.match_info['short_url']
    original_link = await get_from_db(app=request.app, url=url)
    raise aiohttp.web.HTTPFound(original_link[0].get('original_link'))
