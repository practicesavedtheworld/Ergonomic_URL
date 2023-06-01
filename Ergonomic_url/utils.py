import logging
import string

import aiohttp.web
import asyncpg
from asyncpg import Record


def get_short_link(link: str, app: aiohttp.web.Application) -> str:
    """Generates unique short link for every 'long link' in a form host:port/symbols.
    Every link has only one unique short link"""
    def get_unique_short_link_piece(link: str) -> str:
        """The following algorithm return unique sequence of symbols"""
        chars = (string.digits + string.ascii_letters).replace('l', '').replace('I', '')
        len_url, len_chars, right_piece, rem = len(link), len(chars), link[len(link) // 2:], -len(link) % len(chars)
        symbols = [chars[rem]]

        while len_chars:
            _, len_chars = divmod(len_url, len_chars)
            symbols.append(chars[len_chars])
        symbols.append((right_piece[0] + right_piece[-1]).replace('/', '.'))
        symbols.reverse()
        return ''.join(symbols)

    config = app['config']
    new_link = '{host}:{port}/{other}'.format(host=config['host'],
                                              port=config['port'],
                                              other=get_unique_short_link_piece(link))
    return new_link


async def push_to_db(app: aiohttp.web.Application, original_url: str) -> str:
    """Pushing value to DB if it's doesnt there using transaction"""
    db: asyncpg.Pool = app['db']
    async with db.acquire() as connection:
        try:
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
        except asyncpg.InvalidTransactionStateError as t_err:
            logging.error('Something blocks transaction', exc_info=t_err)
            raise
        except asyncpg.PostgresError as err:
            logging.error(f'Failed transaction {query_from} or {query_into}', exc_info=err)
            raise


async def get_from_db(app: aiohttp.web.Application, url: str) -> list[Record]:
    """Get link from db using transaction"""
    db: asyncpg.Pool = app['db']
    async with db.acquire() as connection:
        try:
            async with connection.transaction():
                original_link_query = """
                    SELECT original_link FROM links WHERE short_link = $1;
                """
                link: list[Record] = await connection.fetch(original_link_query, url)
                return link
        except asyncpg.InvalidTransactionStateError as t_err:
            logging.error('Something blocks transaction', exc_info=t_err)
            raise
        except asyncpg.PostgresError as err:
            logging.error(f'Failed transaction {original_link_query}', exc_info=err)
            raise
