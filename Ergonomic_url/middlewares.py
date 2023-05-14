import logging

from aiohttp import web
from aiohttp.web import Request


@web.middleware
async def link_middleware(request: Request, handler):
    try:
        return await handler(request)
    except web.HTTPException as err:
        logging.error('', exc_info=err)
        raise
    except Exception:
        raise web.HTTPNotFound()
