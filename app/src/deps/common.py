import fastapi

from src.database import async_session, Db


async def get_db(request: fastapi.Request) -> Db:
    session: Db = async_session()
    # save to terminate session in middleware before returning response
    request.state.db_session = session
    yield session
