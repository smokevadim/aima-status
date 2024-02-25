from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.dto import CityDTO
from db.models import CityModel


async def get_list(session: AsyncSession):
    query = await session.execute(select(CityModel))
    entities = query.scalars().all()
    return [CityDTO.model_validate(_) for _ in entities]
