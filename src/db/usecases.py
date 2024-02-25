from db.adapters import cities
from db.connection import get_session


async def get_cities():
    async with get_session() as session:
        return await cities.get_list(session)
