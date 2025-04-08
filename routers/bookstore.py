from fastapi import APIRouter, Depends, Request, status, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app_task2.schemas.bookstore import CreateBookstore, UpdateBookstore, BookstoreResponse
from app_task2.services.bookstore import BookstoreService
from app_task2.database import get_database

bookstore_router = APIRouter(tags=["Bookstores"])
logger = logging.getLogger(__name__)

def bookstore_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return BookstoreService(db)

@bookstore_router.post("/create_bookstore", response_model=BookstoreResponse, status_code=201)
async def create_bookstore(request: Request, bookstore: CreateBookstore, service: BookstoreService = Depends(bookstore_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.create_bookstore(bookstore)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e: 
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@bookstore_router.get("/get_bookstores", response_model=List[BookstoreResponse])
async def get_bookstores(request: Request, service: BookstoreService = Depends(bookstore_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_bookstores()
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e: 
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@bookstore_router.get("/get_bookstore/{bookstore_id}", response_model=BookstoreResponse)
async def get_bookstore(request: Request, bookstore_id: str, service: BookstoreService = Depends(bookstore_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_bookstore(bookstore_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e: 
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@bookstore_router.put("/update_bookstore/{bookstore_id}", response_model=BookstoreResponse)
async def update_bookstore(request: Request, bookstore_id: str, bookstore_update: UpdateBookstore, service: BookstoreService = Depends(bookstore_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.update_bookstore(bookstore_id, bookstore_update)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e: 
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    

@bookstore_router.delete("/delete_bookstore/{bookstore_id}", status_code=204)
async def delete_bookstore(request: Request, bookstore_id: str, service: BookstoreService = Depends(bookstore_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_bookstore(bookstore_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e: 
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@bookstore_router.post("/add_bookstore_book/{bookstore_id}/books/{book_id}", response_model=BookstoreResponse)
async def add_book_to_bookstore(request: Request, bookstore_id: str, book_id: str, service: BookstoreService = Depends(bookstore_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.add_book_to_bookstore(bookstore_id, book_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e: 
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@bookstore_router.delete("/delete_bookstore_book/{bookstore_id}/books/{book_id}", response_model=BookstoreResponse)
async def remove_book_from_bookstore(request: Request, bookstore_id: str, book_id: str, service: BookstoreService = Depends(bookstore_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.remove_book_from_bookstore(bookstore_id, book_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e: 
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


# @bookstore_router.get("/base/{bookstore_id}", response_model=BaseBookstoreResponse)
# async def get_base_bookstore(bookstore_id: str, service: BookstoreService = Depends(bookstore_service)):
#     return await service.get_base_bookstore(bookstore_id)