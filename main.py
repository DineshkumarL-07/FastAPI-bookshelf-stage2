from fastapi import FastAPI
from app_task2.routers.books import book_router
from app_task2.routers.authors import author_router
from app_task2.routers.categories import categories_router
from app_task2.routers.reviews import review_router
from app_task2.routers.bookstore import bookstore_router
from app_task2.routers.users import user_router
from app_task2.routers.publisher import publisher_router

app = FastAPI()
app.include_router(book_router)
app.include_router(author_router)
app.include_router(categories_router)
app.include_router(review_router)
app.include_router(bookstore_router)
app.include_router(user_router)
app.include_router(publisher_router)