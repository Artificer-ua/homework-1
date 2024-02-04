import pickle

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from ..conf.config import config
from ..database.connect import get_db
from ..entity.models import User
from ..repository import users as repositories_users
from ..schemas.user import UserResponse
from ..services.auth import auth_service

router_users = APIRouter(prefix="/users", tags=["users"])


@router_users.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    return user


@router_users.patch("/avatar", response_model=UserResponse)
async def update_avatar_user(
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
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
