import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.carbon import CarbonEntry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_data(db: AsyncSession):
    # Check if data already exists
    pass

async def main():
    logger.info("Seeding data...")
    async with AsyncSessionLocal() as session:
        await seed_data(session)
        await session.commit()
    logger.info("Seeding complete.")

if __name__ == "__main__":
    asyncio.run(main())
