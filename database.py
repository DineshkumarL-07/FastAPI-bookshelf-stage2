import os
from motor.motor_asyncio import AsyncIOMotorClient


async def get_database():
    mongo_url = os.getenv('MONGO_URL')
    client = AsyncIOMotorClient(mongo_url)
    db = client['bookshelf_updated']
    yield db
    client.close()