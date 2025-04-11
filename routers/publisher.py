from fastapi import APIRouter, Depends, HTTPException, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from schemas.publisher import CreatePublisher, UpdatePublisher, PublisherResponse
from services.publisher import PublisherService
from database import get_database

publisher_router = APIRouter(tags=['Publisher'])
logger = logging.getLogger(__name__)

def publisher_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return PublisherService(db)

@publisher_router.post("/create_publisher", response_model=PublisherResponse, status_code=status.HTTP_201_CREATED)
async def create_publisher(request: Request, publisher: CreatePublisher, service: PublisherService = Depends(publisher_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.create_publisher(publisher)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@publisher_router.get("/get_publisher/{publisher_id}", response_model=PublisherResponse, status_code=status.HTTP_201_CREATED)
async def get_publisher(request: Request, publisher_id: str, service: PublisherService = Depends(publisher_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_publisher(publisher_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@publisher_router.get("/get_publishers", response_model=List[PublisherResponse], status_code=status.HTTP_201_CREATED)
async def get_publisher(request: Request, service: PublisherService = Depends(publisher_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_publishers()
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@publisher_router.put("/update_publisher/{publisher_id}", response_model=PublisherResponse, status_code=status.HTTP_201_CREATED)
async def update_publisher(request: Request, publisher_id: str, publisher_data: UpdatePublisher,  service: PublisherService = Depends(publisher_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.update_publisher(publisher_id=publisher_id, update_data=publisher_data) 
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@publisher_router.delete("/delete_publisher/{publisher_id}", response_model=PublisherResponse, status_code=status.HTTP_201_CREATED)
async def delete_publisher(request: Request, publisher_id: str,  service: PublisherService = Depends(publisher_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.delete_publisher(publisher_id=publisher_id) 
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")