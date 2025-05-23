from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from models.publisher import Publisher
from schemas.publisher import CreatePublisher, UpdatePublisher, PublisherResponse
# from services import BaseService
from datetime import datetime

class PublisherService():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db['publishers']
        self.book_collection = db['books']

    def _replace_id(self, doc):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return doc

    async def create_publisher(self, publisher_data: CreatePublisher) -> PublisherResponse:
        # existing = await self.collection.find_one({"name": publisher_data.name})
        # if existing:
        #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Publisher with this name already exists.")
        publisher = Publisher(**publisher_data.model_dump())
        result = await self.collection.insert_one(publisher.model_dump())
        created_publisher = await self.collection.find_one({"_id": result.inserted_id})
        return await self._to_response(created_publisher)

    async def get_publisher(self, publisher_id: str) -> PublisherResponse:
        try:
            publisher = await self.collection.find_one({"_id": ObjectId(publisher_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not publisher:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found")
        return await self._to_response(publisher)

    async def update_publisher(self, publisher_id: str, update_data: UpdatePublisher) -> PublisherResponse:
        try:
            update_dict = update_data.model_dump(exclude_unset=True)
            update_dict["updated_at"] = datetime.now()
            result = await self.collection.update_one({"_id": ObjectId(publisher_id)}, {"$set": update_dict})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found")
        updated_publisher = await self.collection.find_one({"_id": ObjectId(publisher_id)})
        return await self._to_response(updated_publisher)

    async def delete_publisher(self, publisher_id: str) -> None:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(publisher_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found")

    async def get_publishers(self) -> list:
        publishers = await self.collection.find().to_list(None)
        return [await self._to_response(publisher) for publisher in publishers]

    async def _to_response(self, doc) -> PublisherResponse:
        doc = self._replace_id(doc)

        books_cursor = await self.book_collection.find({"publisher_id": doc["id"]}).to_list(None)
        books = [{"id": str(book["_id"]), "name": book.get("title")} for book in books_cursor]

        doc["books"] = books
        return PublisherResponse(**doc)
    
    # async def get_base_publisher(self, publisher_id: str) -> BasePublisherResponse:
    #     try:
    #         publisher = await self.collection.find_one({"_id": ObjectId(publisher_id)})
    #     except InvalidId:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
    #     if not publisher:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found")
    #     publisher = self._replace_id(publisher)
    #     return BasePublisherResponse(**{"id": publisher["id"], "name": publisher.get("name")})