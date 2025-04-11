from fastapi import FastAPI
from routers.books import book_router
from routers.authors import author_router
from routers.categories import categories_router
from routers.reviews import review_router
from routers.bookstore import bookstore_router
from routers.users import user_router
from routers.publisher import publisher_router

app = FastAPI()
app.include_router(book_router)
app.include_router(author_router)
app.include_router(categories_router)
app.include_router(review_router)
app.include_router(bookstore_router)
app.include_router(user_router)
app.include_router(publisher_router)