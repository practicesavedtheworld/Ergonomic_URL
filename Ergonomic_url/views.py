import aiohttp.web
import aiohttp_jinja2
from aiohttp.web_request import Request
from utils import push_to_db

@aiohttp_jinja2.template('index.html')
async def index(request: Request):
    return {'name': 'Ergonomic your URL'}

async def ergonomic(request: Request):
    data = await request.json()
    print(data)
    original_link = data['url']
    short_link = await push_to_db(request.app, original_link)

    print('ORIGINAL LINK IS ->>', original_link)
    return aiohttp.web.json_response({'url': short_link})