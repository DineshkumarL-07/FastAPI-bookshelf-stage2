from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from models.user import User
from schemas.user import CreateUser, UpdateUser, UserResponse
# from app_task2.services import BaseService
from services.books import BookService
from services.reviews import ReviewService
from datetime import datetime

class UserService():
    
    def __init__(self, db:AsyncIOMotorDatabase):
        self.db = db
        self.collection = db['users']
        self.book_service = BookService(db)
        self.review_service = ReviewService(db)

    def _replace_id(self, doc):
        doc['id'] = str(doc.pop('_id'))
        return doc
    
    async def create_user(self, user_data:CreateUser):
        user_dict = user_data.model_dump()
        user_dict.update({ 
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        })
        user = User(**user_dict)
        result = await self.collection.insert_one(user.model_dump())
        user = await self.collection.find_one({'_id':result.inserted_id})
        return await self._to_response(user)
    
    async def get_user(self, user_id: str):
        try:
            user = await self.collection.find_one({'_id': ObjectId(user_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return await self._to_response(user)

    async def get_users(self):
        users = await self.collection.find().to_list(None)
        return [self._to_response(user) for user in users]
    
    async def update_user(self, user_id: str, update_data: UpdateUser):
        try:
            result = await self.collection.update_one({'_id': ObjectId(user_id)},
                                                      {'$set': update_data.dict(exclude_unset=True)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user = await self.collection.find_one({'_id': ObjectId(user_id)})
        return await self._to_response(user)
    
    async def delete_user(self, user_id: str):
        try:
            result = await self.collection.delete_one({'_id': ObjectId(user_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UserID")
        
    async def get_users(self):
        users = await self.collection.find().to_list(None)
        return [await self._to_response(user) for user in users]

    async def _to_response(self, doc):
        doc = self._replace_id(doc)

        favorite_books = []
        total_reviews = 0

        user_id = doc["id"]
        if user_id:
            favorite_books_cursor = self.book_service.collection.find(
                {"user_id": user_id, "is_favorite": True},
                {"_id": 1, "title": 1}
            ).limit(5)
            favorite_books = [
                {"id": str(book["_id"]), "title": book["title"]}
                async for book in favorite_books_cursor
            ]

            total_reviews = await self.review_service.collection.count_documents({"created_by": user_id})

        doc["favorite_books"] = favorite_books
        doc["total_reviews"] = total_reviews

        doc.setdefault("name", "Unknown")
        doc.setdefault("email", "Unknown")
        doc.setdefault("gender", "Unknown")
        doc.setdefault("phone_number", "Unknown")
        doc.setdefault("age", 0)
        doc.setdefault("created_at", "Unknown")
        doc.setdefault("updated_at", "Unknown")

        return UserResponse(**doc)
    
    # async def get_base_user(self, user_id: str):
    #     try:
    #         user = await self.collection.find_one({'_id': ObjectId(user_id)})
    #     except InvalidId:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
    #     if not user:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    #     user = self._replace_id(user)
    #     return BaseUserResponse(**user)