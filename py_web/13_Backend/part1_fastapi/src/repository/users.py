import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..entity.models import User
from ..schemas.user import UserSchema

# from libgravatar import Gravatar



async def get_user_by_email(email: str, db: AsyncSession):
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    return user.scalar_one_or_none()


async def create_user(body: UserSchema, db: AsyncSession):
    avatar = None

    # try:
    #     g = Gravatar(body.email)
    #     avatar = g.get_image()
    # except Exception as e:
    #     print(e)

    new_user = User(**body.model_dump(), avatar=avatar)
    logging.debug(f"new_user: {new_user}")
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    logging.debug(f"new_user: {new_user}")
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar(email, url: str, db: AsyncSession) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user
