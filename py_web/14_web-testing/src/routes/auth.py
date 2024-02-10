from fastapi import (APIRouter, BackgroundTasks, Depends, HTTPException,
                     Request, Security, status)
from fastapi.security import (HTTPAuthorizationCredentials, HTTPBearer,
                              OAuth2PasswordRequestForm)
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf import messages
from src.database.connect import get_db
from src.repository import users as repositories_users
from src.schemas.user import (RequestEmail, TokenSchema, UserResponse,
                              UserSchema)
from src.services.auth import auth_service
from src.services.email import send_email

router_auth = APIRouter(prefix="/auth", tags=["auth"])
get_refresh_token = HTTPBearer()


@router_auth.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
    body: UserSchema,
    bt: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    The signup function creates a new user in the database.

    :param body: UserSchema: Validate the request body
    :param bt: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base url of the request
    :param db: AsyncSession: Get the database session
    :param : Get the user id from the path
    :return: A userschema object, which is a pydantic model
    """
    exist_user = await repositories_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=messages.ACCOUNT_EXISTS
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repositories_users.create_user(body, db)
    bt.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user


@router_auth.post("/login", response_model=TokenSchema)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    The login function is used to authenticate a user.

    :param body: OAuth2PasswordRequestForm: Get the username and password from the request body
    :param db: AsyncSession: Get the database session
    :return: A dictionary with the access_token, refresh_token and token_type
    """
    user = await repositories_users.get_user_by_email(body.username, db)

    # User exists?
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_EMAIL
        )

    # email confirmed?
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.EMAIL_NOT_CONFIRMED,
        )

    # password is ok?
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_PASSWORD
        )

    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})

    await repositories_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router_auth.get("/refresh_token", response_model=TokenSchema)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(get_refresh_token),
    db: AsyncSession = Depends(get_db),
):
    """
    The refresh_token function is used to refresh the access token.
    It takes in a refresh token and returns a new access token.
    The function first decodes the refresh_token to get the email of the user who owns it, then gets that user from our database.
    If we find that this user's stored refresh_token does not match what was passed in, we update their stored tokens with None (logging them out) and raise an error saying &quot;Invalid Refresh Token&quot;.
    Otherwise, we create new tokens for this user using auth_service functions and store them in our database before returning them.

    :param credentials: HTTPAuthorizationCredentials: Get the access token from the request header
    :param db: AsyncSession: Get the database session
    :param : Get the credentials from the request header
    :return: A dict with the access token and refresh token
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repositories_users.get_user_by_email(email, db)

    if user.refresh_token != token:
        await repositories_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repositories_users.update_token(user, refresh_token, db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router_auth.get("/confirmed_email/{token}")
async def confirmed_email(token: str, db: AsyncSession = Depends(get_db)):
    """
    The confirmed_email function is used to confirm a user's email address.
        It takes the token from the URL and uses it to get the user's email address.
        Then, it checks if that user exists in our database, and if they do not exist,
        we raise an HTTPException with a 400 status code (Bad Request) and detail message of &quot;Verification error&quot;.

    :param token: str: Get the token from the request
    :param db: AsyncSession: Get the database session
    :return: A message that the email is already confirmed or a message that the email has been confirmed
    """
    email = await auth_service.get_email_from_token(token)
    user = await repositories_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repositories_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router_auth.post("/request_email")
async def request_email(
    body: RequestEmail,
    bt: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    The request_email function is used to send a confirmation email to the user.
    It takes in an email address, and if that address exists in the database, it sends
    an email with a link for confirming their account. If they are already confirmed,
    it returns an error message.

    :param body: RequestEmail: Validate the request body against the requestemail schema
    :param bt: BackgroundTasks: Add a task to the background tasks
    :param request: Request: Get the base_url of the request
    :param db: AsyncSession: Get the database session
    :param : Get the user's email from the database
    :return: A dictionary with a message
    """
    user = await repositories_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        bt.add_task(send_email, user.email, user.username, str(request.base_url))
    return {"message": "Check your email for confirmation."}


# @router_auth.get('/{username}')
# async def request_email(username: str, rp: Response,  db: AsyncSession = Depends(get_db)):
