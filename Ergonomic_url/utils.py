import aiohttp.web
import string

import asyncpg


def get_short_link(link: str, app: aiohttp.web.Application) -> str:
    def get_unique_short_link_piece(link) -> str:
        chars = (string.digits + string.ascii_letters).replace('l', '').replace('I', '')
        len_s, len_chars, right_piece, rem = len(link), len(chars), link[len(link) // 2:], -len(link) % len(chars)
        symbols = [chars[rem]]

        while len_chars:
            _, len_chars = divmod(len_s, len_chars)
            symbols.append(chars[len_chars])
        symbols.append(right_piece[0] + right_piece[-1])
        symbols.reverse()
        return ''.join(symbols)

    config = app['config']
    new_link = '{host}:{port}/{other}'.format(host=config['host'],
                                              port=config['port'],
                                              other=get_unique_short_link_piece(link))
    return new_link


async def push_to_db(app: aiohttp.web.Application, original_url: str):
    db: asyncpg.Pool = app['db']
    async with db.acquire() as connection:
        async with connection.transaction():
            query_from = """
                SELECT original_link FROM links where original_link = $1;
            """
            result_from = await connection.fetch(query_from, original_url)
            short_link = get_short_link(original_url, app)
            if len(result_from) == 0:
                query_into = """
                    INSERT INTO links (original_link, short_link) VALUES ($1, $2);
                """
                await connection.fetch(query_into, original_url, short_link.rsplit('/', maxsplit=1)[-1])
            return short_link


async def get_from_db(app: aiohttp.web.Application, url: str):
    db: asyncpg.Pool = app['db']
    async with db.acquire() as connection:
        async with connection.transaction():
            original_link_query = """
                SELECT original_link FROM links WHERE short_link = $1;
            """
            link = await connection.fetch(original_link_query, url)
            return link