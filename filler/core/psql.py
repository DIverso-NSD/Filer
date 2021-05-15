import asyncpg

from contextlib import asynccontextmanager

from filler.core.settings import settings


@asynccontextmanager
async def db_connect():
    conn = await asyncpg.connect(settings.psql_url)
    try:
        yield conn
    finally:
        await conn.close()


async def get_user(id: str) -> asyncpg.Record:
    async with db_connect() as conn:
        return await conn.fetchrow(
            "select * from user where id=$1",
            id,
        )


async def create_file_record(
    name: str, size: str, status: str, user_id: str
) -> asyncpg.Record:
    async with db_connect() as conn:
        return await conn.execute(
            "insert into files (name, size, status, user_id) values($1, $2, $3, $4)",
            name,
            size,
            status,
            user_id,
        )


async def patch_file_record(id: str, status: str) -> asyncpg.Record:
    async with db_connect() as conn:
        return await conn.execute(
            "update files set status=$1 where id=$2",
            status,
            id,
        )
