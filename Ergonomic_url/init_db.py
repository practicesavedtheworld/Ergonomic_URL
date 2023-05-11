import aiohttp.web
import asyncpg
import logging

from Exceptions import FailedTableCreation


async def connect_to_db(app: aiohttp.web.Application) -> None:
    db = app['config']['postgres']
    try:
        pool: asyncpg.Pool = await asyncpg.create_pool(user=db['user'],
                                                       database=db['database'],
                                                       password=db['password'],
                                                       min_size=db['minsize'],
                                                       max_size=db['maxsize'],
                                                       host=db['host'],
                                                       port=db['port'],
                                                       )
    except asyncpg.PostgresError as pg_err:
        logging.error("Pool wasn't create, check your configuration", exc_info=pg_err)
        raise
    async with pool.acquire() as connection:
        create_query = """
            CREATE TABLE IF NOT EXISTS links(
            ID BIGSERIAL PRIMARY KEY,
            original_link VARCHAR(300),
            short_link VARCHAR(50)
            );
        """
        status = await connection.execute(create_query)
        if not len(status):
            raise FailedTableCreation('links')

    app['db'] = pool
