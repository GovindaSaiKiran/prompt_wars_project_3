import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.db.session import engine
from app.models.emission_factor import EmissionFactor
import uuid

# Typical EPA/DEFRA values for demonstration
# unit factors are kg CO2e per unit
SEED_FACTORS = [
    {"category": "transport", "activity": "driving_gasoline_car", "factor": 0.411, "unit": "miles", "source": "EPA 2023", "region": "Global"},
    {"category": "transport", "activity": "driving_electric_car", "factor": 0.120, "unit": "miles", "source": "EPA 2023", "region": "Global"},
    {"category": "transport", "activity": "flight_short_haul", "factor": 0.250, "unit": "miles", "source": "DEFRA 2023", "region": "Global"},
    {"category": "transport", "activity": "flight_long_haul", "factor": 0.150, "unit": "miles", "source": "DEFRA 2023", "region": "Global"},
    {"category": "energy", "activity": "electricity_grid", "factor": 0.385, "unit": "kWh", "source": "EPA eGRID 2023", "region": "Global"},
    {"category": "food", "activity": "beef_meal", "factor": 27.0, "unit": "kg", "source": "IPCC", "region": "Global"},
    {"category": "food", "activity": "plant_based_meal", "factor": 2.0, "unit": "kg", "source": "IPCC", "region": "Global"}
]

async def seed():
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        for data in SEED_FACTORS:
            # Check if exists
            result = await session.execute(
                select(EmissionFactor).where(EmissionFactor.activity == data["activity"])
            )
            if not result.scalars().first():
                ef = EmissionFactor(
                    id=str(uuid.uuid4()),
                    category=data["category"],
                    activity=data["activity"],
                    factor=data["factor"],
                    unit=data["unit"],
                    source=data["source"],
                    region=data["region"]
                )
                session.add(ef)
        await session.commit()
        print("Successfully seeded emission factors.")

if __name__ == "__main__":
    asyncio.run(seed())
