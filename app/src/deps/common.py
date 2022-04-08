import fastapi
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session


async def get_db(request: fastapi.Request) -> AsyncSession:
    session: AsyncSession = async_session()
    # save to terminate session in middleware before returning response
    request.state.db_session = session
    yield session
