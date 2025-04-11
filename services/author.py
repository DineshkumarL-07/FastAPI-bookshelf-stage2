from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from models.author import Author
from schemas.author import CreateAuthor, UpdateAuthor, AuthorResponse
# from services import BaseService
from services.books import BookService
from datetime import datetime

class AuthorService():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db['authors']
        self.book_service = BookService(db)  
        
    def _replace_id(self, doc):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return doc

    async def create_author(self, author_data: CreateAuthor):
        author_dict = author_data.model_dump()
        author_dict.update({
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        })
        author = Author(**author_dict)
        result = await self.collection.insert_one(author.model_dump())
        created_author = await self.collection.find_one({"_id": result.inserted_id})
        return await self._to_response(created_author)

    async def get_author(self, author_id: str) -> AuthorResponse:
        try:
            author = await self.collection.find_one({"_id": ObjectId(author_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
        return await self._to_response(author)

    async def update_author(self, author_id: str, update_data: UpdateAuthor) -> AuthorResponse:
        try:
            update_dict = update_data.model_dump(exclude_unset=True)
            update_dict["updated_at"] = datetime.now()
            result = await self.collection.update_one({"_id": ObjectId(author_id)}, {"$set": update_dict})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
        author = await self.collection.find_one({"_id": ObjectId(author_id)})
        return await self._to_response(author)

    async def delete_author(self, author_id: str) -> None:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(author_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid AuthorID")
    
    async def get_authors(self) -> list:
        authors = await self.collection.find().to_list(None)
        return [await self._to_response(author) for author in authors]

    async def _to_response(self, doc) -> AuthorResponse:
        doc = self._replace_id(doc)

        latest_books = []
        total_published = 0
        average_rating = 0.0
        author_id = doc["id"]
        if author_id:
            latest_books_cursor = self.book_service.collection.find(
                {"author_id": author_id},
                {"_id": 1, "title": 1}
            ).sort("created_at", -1).limit(3)
            latest_books = [
                {"id": str(book["_id"]), "title": book["title"]}
                async for book in latest_books_cursor
            ]

            total_published = await self.book_service.collection.count_documents({"author_id": author_id})

            pipeline = [
                {"$match": {"author_id": author_id}},
                {"$lookup": {
                    "from": "reviews",
                    "localField": "_id",
                    "foreignField": "book_id",
                    "as": "reviews"
                }},
                {"$unwind": {"path": "$reviews", "preserveNullAndEmptyArrays": True}},
                {"$group": {
                    "_id": "$author_id",
                    "average_rating": {"$avg": "$reviews.rating"}
                }}
            ]
            agg = await self.book_service.collection.aggregate(pipeline).to_list(length=1)
            average_rating = round(agg[0]["average_rating"], 2) if agg and agg[0].get("average_rating") is not None else 0.0
        doc["latest_books"] = latest_books
        doc["total_published"] = total_published
        doc["average_rating"] = average_rating

        doc.setdefault("name", "Unknown")
        doc.setdefault("age", 0)
        doc.setdefault("gender", "Unknown")
        doc.setdefault("awards", [])

        return AuthorResponse(
            id=doc["id"],
            name=doc["name"],
            age=doc["age"],
            gender=doc["gender"],
            awards=doc["awards"],
            latest_books=doc["latest_books"],
            total_published=doc["total_published"],
            average_rating=doc["average_rating"],
            created_at=doc["created_at"],   
            updated_at=doc["updated_at"]
        )
    
    # async def get_base_author(self, author_id: str) -> BaseAuthorResponse:
    #     try:
    #         author = await self.collection.find_one({"_id": ObjectId(author_id)})
    #     except InvalidId:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
    #     if not author:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    #     author = self._replace_id(author)
    #     return BaseAuthorResponse(**author)