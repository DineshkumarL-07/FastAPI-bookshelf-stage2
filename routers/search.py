from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app_task2.database import get_database

search_router = APIRouter(tags=["Search Operations"])
logger = logging.getLogger(__name__)

def search_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return SearchService(db)