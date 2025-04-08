from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app_task2.models.categories import Category
from app_task2.schemas.categories import CreateCategory, UpdateCategory, CategoryResponse
# from app_task2.services import BaseService
from datetime import datetime

class CategoryService():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db['categories']

    def _replace_id(self, doc):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return doc

    async def _to_response(self, doc) -> CategoryResponse:
        doc = self._replace_id(doc)
        return CategoryResponse(**doc)

    async def create_category(self, category_data: CreateCategory) -> CategoryResponse:
        # existing = await self.collection.find_one({"name": category_data.name})
        # if existing:
        #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category with this name already exists.")
        category = Category(**category_data.model_dump())
        result = await self.collection.insert_one(category.model_dump())
        created_category = await self.collection.find_one({"_id": result.inserted_id})
        return await self._to_response(created_category)

    async def get_category(self, category_id: str) -> CategoryResponse:
        try:
            category = await self.collection.find_one({"_id": ObjectId(category_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return await self._to_response(category)

    async def update_category(self, category_id: str, update_data: UpdateCategory) -> CategoryResponse:
        try:
            update_dict = update_data.model_dump(exclude_unset=True)
            update_dict["updated_at"] = datetime.now()
            result = await self.collection.update_one({"_id": ObjectId(category_id)}, {"$set": update_dict})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        updated_category = await self.collection.find_one({"_id": ObjectId(category_id)})
        return await self._to_response(updated_category)

    async def delete_category(self, category_id: str) -> None:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(category_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    async def get_categories(self) -> list:
        categories = await self.collection.find().to_list(None)
        return [await self._to_response(category) for category in categories]

    # async def get_base_category(self, category_id: str) -> BaseCategoryResponse:
    #     try:
    #         category = await self.collection.find_one({"_id": ObjectId(category_id)})
    #     except InvalidId:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
    #     if not category:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    #     category = self._replace_id(category)
    #     return BaseCategoryResponse(**{"id": category["id"], "name": category.get("name")})