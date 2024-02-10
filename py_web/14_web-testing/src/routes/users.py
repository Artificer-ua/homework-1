import pickle

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import config
from src.database.connect import get_db
from src.entity.models import User
from src.repository import users as repositories_users
from src.schemas.user import UserResponse
from src.services.auth import auth_service

router_users = APIRouter(prefix="/users", tags=["users"])


@router_users.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    """
    The get_current_user function is a dependency that will be injected into the
        get_current_user endpoint. It uses the auth_service to retrieve the current user,
        and returns it if found.

    :param user: User: Get the current user
    :return: The current user, if the user is authenticated
    """
    return user


@router_users.patch("/avatar", response_model=UserResponse)
async def update_avatar_user(
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    The update_avatar_user function is used to update the avatar of a user.
        The function takes in an UploadFile object, which contains the file that will be uploaded to Cloudinary.
        It also takes in a User object, which is obtained from Depends(auth_service.get_current_user). This User object represents the current user who has logged into our application and wants to update their avatar image.
        Finally, it also takes in an AsyncSession object (which we get from Depends(get_db)), so that we can use this session for database operations.

    :param file: UploadFile: Get the file from the request
    :param current_user: User: Get the current user from the database
    :param db: AsyncSession: Connect to the database
    :param : Get the current user
    :return: The updated user
    """
    cloudinary.config(
        cloud_name=config.CLOUDINARY_NAME,
        api_key=config.CLOUDINARY_API_KEY,
        api_secret=config.CLOUDINARY_API_SECRET,
        secure=True,
    )

    public_id = f"WEB17/{current_user.username}"
    resource = cloudinary.uploader.upload(
        file.file, public_id=public_id, overwrite=True
    )
    resource_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=resource.get("version")
    )
    user = await repositories_users.update_avatar(current_user.email, resource_url, db)
    auth_service.cache.set(user.email, pickle.dumps(user))
    auth_service.cache.expire(user.email, 300)
    return user
