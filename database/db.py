from alembic import command
from alembic.config import Config
from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from settings import DatabaseSettings

database_url = DatabaseSettings().DATABASE_URL # pyright: ignore[reportCallIssue]
engine = create_async_engine(database_url)

def run_upgrade(connection: Connection, config: Config):
    config.attributes["connection"] = connection
    command.upgrade(config, "head")

async def run_migrations():
    config = Config("alembic.ini")
    config.set_main_option('sqlalchemy.url', str(engine.url))
    
    async with engine.connect() as connection:
        await connection.run_sync(run_upgrade, config)
    