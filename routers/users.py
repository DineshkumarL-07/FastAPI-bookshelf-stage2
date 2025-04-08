from fastapi import APIRouter, Depends, HTTPException, Request, status, Path
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app_task2.schemas.user import CreateUser, UserResponse, UpdateUser
from app_task2.database import get_database
from app_task2.services.user import UserService

user_router = APIRouter(tags = ['Users'])
logger = logging.getLogger(__name__)

def user_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return UserService(db)


@user_router.post('/create_user',response_model = UserResponse)
async def create_user(request:Request, user : CreateUser, service:UserService=Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.create_user(user)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@user_router.get('/get_user/{user_id}',response_model = UserResponse)
async def get_user_details(request:Request, user_id:str=Path(...), service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        user = await service.get_user(user_id=user_id)
        return user
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@user_router.get('/get_users', response_model=List[UserResponse])
async def get_users(request:Request, service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_users()
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@user_router.put("/update_user/{user_id}",response_model = UserResponse)
async def update_user(request:Request, user_id:str, user : UpdateUser, service:UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        user_update = await service.update_user(user_id=user_id,update_data=user)
        return user_update
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@user_router.delete('/delete_user/{user_id}')
async def delete_user(request : Request, user_id : str, service : UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_user(user_id=user_id)
        return f"user with id {user_id} is successfully deleted"
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@user_router.get("/get_user/{user_id}/favorite_books", response_model=List[str])
async def get_user_favorite_books(request: Request, service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.get_user_favorite_books()
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@user_router.post("/get_user/{user_id}/favorite_books/{book_id}", response_model=List[str])
async def create_user_favorite_book_details(request: Request, user_id: str,book_id: str, service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.create_user_favorite_book_details(user_id, book_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@user_router.delete("/get_user/{user_id}/favorite_books/{book_id}")
async def delete_user_favorite_book_details(request: Request,user_id: str, book_id: str, service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_user_favorite_book_details(user_id, book_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")