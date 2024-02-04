# import logging
from ipaddress import ip_address
from typing import Callable

import redis.asyncio as redis
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.conf.config import config
from src.database.connect import get_db
from src.routes import auth, contacts, todos, users
from starlette import status

# import re



app = FastAPI()

ALLOWED_IPS = [ip_address("127.0.0.1")]
# banned_ips = [ip_address("192.168.1.1"), ip_address("192.168.1.2"), ip_address("127.0.0.2")]
# user_agent_ban_list = [r"Gecko", r"Python-urllib"]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# static files
app.mount("/static", StaticFiles(directory="src/static"), name="status")

app.include_router(auth.router_auth, prefix="/api")
app.include_router(todos.router_todo, prefix="/api")
app.include_router(contacts.router_contact, prefix="/api")
app.include_router(users.router_users, prefix="/api")

# logging.basicConfig(
#     format="%(asctime)s %(message)s",
#     level=logging.INFO,
#     handlers=[
#         logging.FileHandler("file.log"),
#         # logging.StreamHandler()
#     ],
# )


# @app.middleware("http")
# async def ban_ips(request: Request, call_next: Callable):
#     ip = ip_address(request.client.host)
#     if ip in banned_ips:
#         return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
#     response = await call_next(request)
#     return response


@app.middleware("http")
async def limit_access_by_ip(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    if ip not in ALLOWED_IPS:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Not allowed IP address"},
        )
    response = await call_next(request)
    return response


# @app.middleware("http")
# async def user_agent_ban_middleware(request: Request, call_next: Callable):
#     user_agent = request.headers.get("user-agent")
#     for ban_pattern in user_agent_ban_list:
#         if re.search(ban_pattern, user_agent):
#             return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
#     response = await call_next(request)
#     return response


@app.on_event("startup")
async def startup():
    r = await redis.Redis(
        host=config.REDIS_DOMAIN,
        port=config.REDIS_PORT,
        db=0,
        encoding="utf-8",
        decode_responses=True,
        password=config.REDIS_PASSWORD,
    )
    await FastAPILimiter.init(r)


@app.get("/")
def index():
    return {"message": "Todo Application"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        print(result)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )
