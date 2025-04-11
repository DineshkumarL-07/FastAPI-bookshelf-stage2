# app/services/reviews.py
from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from models.reviews import Review
from schemas.reviews import CreateReview, UpdateReview, ReviewResponse
# from services import BaseService
from datetime import datetime

class ReviewService():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db['reviews']

    def _replace_id(self, doc):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return doc

    async def create_review(self, review_data: CreateReview) -> ReviewResponse:
        review_dict = review_data.model_dump()
        review_dict.update({
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        })
        review = Review(**review_dict)
        result = await self.collection.insert_one(review.model_dump())
        created_review = await self.collection.find_one({'_id': result.inserted_id})
        return await self._to_response(created_review)

    async def get_review(self, review_id: str) -> ReviewResponse:
        try:
            review = await self.collection.find_one({'_id': ObjectId(review_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return await self._to_response(review)

    async def update_review(self, review_id: str, update_data: UpdateReview) -> ReviewResponse:
        try:
            update_dict = update_data.model_dump(exclude_unset=True)
            from datetime import datetime
            update_dict["updated_at"] = datetime.now()
            result = await self.collection.update_one({'_id': ObjectId(review_id)}, {'$set': update_dict})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        review = await self.collection.find_one({'_id': ObjectId(review_id)})
        return await self._to_response(review)

    async def delete_review(self, review_id: str) -> None:
        try:
            result = await self.collection.delete_one({'_id': ObjectId(review_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    async def get_reviews(self) -> list:
        reviews = await self.collection.find().to_list(None)
        return [await self._to_response(review) for review in reviews]
    
    async def _to_response(self, doc) -> ReviewResponse:
        doc = self._replace_id(doc)

        try:
            user = await self.db['users'].find_one({'_id': ObjectId(doc["created_by"])})
        except Exception:
            user = None

        try:
            book = await self.db['books'].find_one({'_id': ObjectId(doc["book_id"])})
        except Exception:
            book = None

        doc['created_by'] = {
            "id": doc["created_by"],
            "name": user["name"] if user else "Unknown"
        }

        doc['book_id'] = {
            "id": doc["book_id"],
            "name": book["title"] if book else "Unknown"
        }

        doc['review_details'] = {
            "likes": doc.get("likes", 0),
            "comments": doc.get("comments", [])
        }

        return ReviewResponse(**doc)

    # async def get_base_review(self, review_id: str) -> BaseReviewResponse:
    #     try:
    #         review = await self.collection.find_one({'_id': ObjectId(review_id)})
    #     except InvalidId:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
    #     if not review:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    #     review = self._replace_id(review)
    #     return BaseReviewResponse(**review)