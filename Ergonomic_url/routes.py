import aiohttp.web
import pathlib

from views import index, ergonomic, redirect

def setup_routes(app: aiohttp.web.Application):
    router = app.router
    router.add_get('/', index)
    router.add_post('/ergonomic', ergonomic)
    router.add_get('/{short_url}', redirect)
    router.add_static('/static/', pathlib.Path(__file__).parent.parent / 'static', name='static')
