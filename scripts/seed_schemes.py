"""
Seeding script to load sbi_schemes.json data into Postgres and ChromaDB databases.
"""
import asyncio
import json
import os
from app.db.postgres import AsyncSessionLocal, init_db
from app.models.scheme import Scheme
from app.db.chromadb_client import get_chroma_client

async def seed():
    print("Initializing databases...")
    await init_db()
    
    # Load from json
    json_path = os.path.join(os.path.dirname(__file__), "../app/data/schemes/sbi_schemes.json")
    with open(json_path, "r") as f:
        schemes_data = json.load(f)
        
    async with AsyncSessionLocal() as session:
        for item in schemes_data:
            scheme = Scheme(
                id=item["scheme_id"],
                name=item["name"],
                category=item["category"],
                max_amount=item["max_amount"],
                interest_rate_percent=item["interest_rate_percent"],
                eligibility_rules=item["eligibility_rules"]
            )
            await session.merge(scheme)
        await session.commit()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    asyncio.run(seed())
