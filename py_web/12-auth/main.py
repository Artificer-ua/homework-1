# import logging

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connect import get_db
from src.routes import auth, contacts

app = FastAPI()

app.include_router(auth.router_auth, prefix="/api")
app.include_router(contacts.router_contact, prefix="/api")

# logging.basicConfig(
#     format="%(asctime)s %(message)s",
#     level=logging.INFO,
#     handlers=[
#         logging.FileHandler("file.log"),
#         # logging.StreamHandler()
#     ],
# )


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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error connecting to the database")













