# import logging
# import sys
# from os.path import abspath, dirname, join

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from libgravatar import Gravatar

# sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from schemas.user import UserSchema
from src.database.connect import get_db
from src.entity.models import User


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    return user.scalar_one_or_none()


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    avatar = None

    # try:
    #     g = Gravatar(body.email)
    #     avatar = g.get_image()
    # except Exception as e:
    #     print(e)

    new_user = User(**body.model_dump(), avatar=avatar)
    # logging.debug(f"new_user: {new_user}")
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession = Depends(get_db)):
    user.refresh_token = token
    await db.commit()