import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import User
from src.schemas.user import UserSchema

# from libgravatar import Gravatar


async def get_user_by_email(email: str, db: AsyncSession):
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user with that email. If no such user exists, it returns None.

    :param email: str: Pass in the email address of the user we want to retrieve
    :param db: AsyncSession: Pass the database session into the function
    :return: A user object or none
    """
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    return user.scalar_one_or_none()


async def create_user(body: UserSchema, db: AsyncSession):
    """
    The create_user function creates a new user in the database.

    :param body: UserSchema: Validate the request body
    :param db: AsyncSession: Create a database session
    :return: A user object
    """
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
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Identify the user that is being updated
    :param token: str | None: Specify that the token parameter can either be a string or none
    :param db: AsyncSession: Pass the database session to the function
    :return: The user object
    """
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.


    :param email: str: Specify the email address of the user to confirm
    :param db: AsyncSession: Pass in the database connection
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar(email, url: str, db: AsyncSession) -> User:
    """
    The update_avatar function updates the avatar of a user.

    :param email: Get the user from the database
    :param url: str: Specify the type of data that is being passed into the function
    :param db: AsyncSession: Pass the database session to the function
    :return: A user object
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user
