from fastapi import APIRouter, Depends, HTTPException, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from schemas.reviews import CreateReview, UpdateReview, ReviewResponse
from services.reviews import ReviewService
from database import get_database

review_router = APIRouter(tags=['Reviews'])
logger = logging.getLogger(__name__)

def review_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return ReviewService(db)

@review_router.post("/create_review", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(request: Request, review: CreateReview, service: ReviewService = Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.create_review(review)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@review_router.get("/get_reviews", response_model=List[ReviewResponse])
async def get_reviews(request: Request, service: ReviewService = Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_reviews()
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@review_router.get("/get_review/{review_id}", response_model=ReviewResponse)
async def get_review(request: Request, review_id: str, service: ReviewService = Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_review(review_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@review_router.put("/update_review/{review_id}", response_model=ReviewResponse)
async def update_review(request: Request, review_id: str, review: UpdateReview, service: ReviewService = Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.update_review(review_id, review)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@review_router.delete("/delete_review/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(request: Request, review_id: str, service: ReviewService = Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_review(review_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")