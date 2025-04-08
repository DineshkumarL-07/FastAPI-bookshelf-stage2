from fastapi import APIRouter, Depends, HTTPException, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app_task2.schemas.categories import CreateCategory, UpdateCategory, CategoryResponse
from app_task2.services.categories import CategoryService
from app_task2.database import get_database

categories_router = APIRouter(tags=['Updated_categories'])
logger = logging.getLogger(__name__)

def categories_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return CategoryService(db)

@categories_router.post("/create_category", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(request: Request, category: CreateCategory, service: CategoryService = Depends(categories_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.create_category(category)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@categories_router.get("/get_categories", response_model=List[CategoryResponse])
async def get_categories(request: Request, service: CategoryService = Depends(categories_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_categories()
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@categories_router.get("/get_category/{categorie_id}", response_model=CategoryResponse)
async def get_category(request: Request, categorie_id: str, service: CategoryService = Depends(categories_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        categorie = await service.get_category(categorie_id)
        return categorie
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@categories_router.put("/update_category/{categorie_id}", response_model=CategoryResponse)
async def update_category(request: Request, categorie_id: str, categorie: UpdateCategory, service: CategoryService = Depends(categories_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        updated_categorie = await service.update_category(categorie_id, categorie)
        return updated_categorie
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@categories_router.delete("/delete_category/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(request: Request, category_id: str, service: CategoryService = Depends(categories_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_category(category_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")