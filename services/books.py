from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app_task2.models.book import Book
from app_task2.schemas.book import BookCreate, BookUpdate, BookResponse
from datetime import datetime

class BookService():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db['books']
        self.reviews = db['reviews']
        self.authors = db['authors']
        self.categories = db['categories']
        self.publishers = db['publishers']
    
    async def create_book(self, book_data: BookCreate):
        # is_exist = await self.collection.find_one({'title' : book_data.title})
        # if is_exist:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book is already available")
        book_datas = book_data.model_dump()
        book_datas.update({
            "created_at" : datetime.now(),
            "updated_at" : datetime.now()
        })
        book = Book(**book_datas)
        result = await self.collection.insert_one(book.model_dump())
        book = await self.collection.find_one({"_id": result.inserted_id})
        return await self._to_response(book)
    
    async def get_book(self, book_id: str):
        try:
            book = await self.collection.find_one({'_id': ObjectId(book_id)})
            print(f"Book fetched: {book}")
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return await self._to_response(book)

    async def get_books(self) -> list:
        books = await self.collection.find().to_list(None)
        return [await self._to_response(book) for book in books]

    async def update_book(self, book_id: str, update_data: BookUpdate):
        try:
            update_data = update_data.model_dump(exclude_unset=True)
            update_data['updated_at'] = datetime.now()
            result = await self.collection.update_one({'_id': ObjectId(book_id)},
                                                      {'$set': update_data})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        book = await self.collection.find_one({'_id': ObjectId(book_id)})
        return await self._to_response(book)
     
    async def delete_book(self, book_id: str):
        try:
            result = await self.collection.delete_one({'_id': ObjectId(book_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    async def _to_response(self, book: dict) -> BookResponse:
        try:
            author = await self.authors.find_one({"_id": ObjectId(book["author_id"])})
        except Exception:
            author = None
        try:
            category = await self.categories.find_one({"_id": ObjectId(book["category_id"])})
        except Exception:
            category = None
        publisher = None
        if book["publisher_id"]:
            try:
                publisher = await self.publishers.find_one({"_id": ObjectId(book["publisher_id"])})
            except Exception:
                publisher = None
        is_published = True if publisher else False

        pipeline = [
            {"$match": {"book_id": str(book["_id"])}},
            {"$group": {"_id": "$book_id", "average": {"$avg": "$rating"}, "count": {"$sum": 1}}}
        ]
        agg = await self.reviews.aggregate(pipeline).to_list(length=1)
        average_rating = round(agg[0]["average"], 2) if agg else None
        total_reviews = agg[0]["count"] if agg else None

        book["id"] = str(book["_id"])
        del book["_id"]

        return BookResponse(
            id=book["id"],
            title=book["title"],
            description=book["description"],
            isbn=book["isbn"],
            author={
                "id": str(author["_id"]) if author else None,
                "name": author["name"] if author else "Unknown"
            },
            category={
                "id": str(category["_id"]) if category else None, 
                "name": category["name"] if category else "Unknown"
            },
            publisher={
                "id": str(publisher["_id"]) if publisher else None,
                "name": publisher["name"] if publisher else None,
            },
            is_published=is_published,
            average_rating=average_rating,
            total_reviews=total_reviews,
            created_at=book["created_at"],
            updated_at=book["updated_at"]
        )