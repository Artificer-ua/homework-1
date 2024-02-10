from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.messages import ITEM_NOT_FOUND
from src.database.connect import get_db
from src.entity.models import User
from src.repository import contacts as repositories_contacts
from src.schemas.contact import ContactResponse, ContactSchema
from src.services.auth import auth_service

router_contact = APIRouter(prefix="/contacts", tags=["contacts"])


@router_contact.get(
    "/",
    response_model=list[ContactResponse],
    dependencies=[Depends(RateLimiter(times=20, seconds=60))],
)
async def get_contacts(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The get_contacts function returns a list of contacts for the current user.

    :param limit: int: Limit the number of contacts returned
    :param ge: Set a minimum value for the limit parameter
    :param le: Limit the number of contacts returned to 500
    :param offset: int: Specify the number of records to skip
    :param ge: Specify a minimum value for the parameter
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: User: Get the user from the database
    :param : Get the contact id from the path
    :return: A list of contacts
    """
    contacts = await repositories_contacts.get_contacts(limit, offset, db, current_user)
    return contacts


@router_contact.get(
    "/{contact_id}",
    response_model=ContactResponse,
    dependencies=[Depends(RateLimiter(times=20, seconds=60))],
)
async def get_contact(
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The get_contact function returns a contact by its ID.

    :param contact_id: int: Get the contact id from the url path
    :param db: AsyncSession: Pass the database connection to the function
    :param current_user: User: Get the current user
    :param : Get the contact id from the url
    :return: A contact object
    """
    contact = await repositories_contacts.get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ITEM_NOT_FOUND
        )
    return contact


@router_contact.post(
    "/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def create_contact(
    body: ContactSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactSchema: Validate the request body
    :param db: AsyncSession: Pass the database connection to the function
    :param current_user: User: Get the current user from the database
    :param : Get the contact id from the url
    :return: A contact object
    """
    contact = await repositories_contacts.create_contact(body, db, current_user)
    return contact


@router_contact.put("/{contact_id}")
async def update_contact(
    body: ContactSchema,
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_contact function updates a contact in the database.

    :param body: ContactSchema: Validate the request body
    :param contact_id: int: Identify the contact to be deleted
    :param db: AsyncSession: Pass the database session to the repository
    :param current_user: User: Get the user that is currently logged in
    :param : Get the contact id from the url
    :return: A contact
    """
    contact = await repositories_contacts.update_contact(
        contact_id, body, db, current_user
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ITEM_NOT_FOUND
        )
    return contact


@router_contact.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The delete_contact function deletes a contact from the database.

    :param contact_id: int: Specify the id of the contact to be deleted
    :param db: AsyncSession: Pass the database session to the repository
    :param current_user: User: Get the user from the database
    :param : Get the contact id from the url
    :return: The deleted contact
    """
    contact = await repositories_contacts.delete_contact(contact_id, db, current_user)
    return contact


@router_contact.get(
    "/search/{search_string}",
    response_model=list[ContactResponse],
    dependencies=[Depends(RateLimiter(times=2, seconds=10))],
)
async def search_contact(
    search_string: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The search_contact function searches for a contact in the database.
        It takes a search_string as an argument and returns the first contact that matches it.

    :param search_string: str: Search for a contact in the database
    :param db: AsyncSession: Get the database session
    :param current_user: User: Get the user that is currently logged in
    :param : Get the contact id
    :return: A single contact
    """
    contact = await repositories_contacts.search_contact(
        search_string, db, current_user
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ITEM_NOT_FOUND
        )
    return contact


@router_contact.get(
    "/search/",
    response_model=list[ContactResponse],
    dependencies=[Depends(RateLimiter(times=2, seconds=10))],
)
async def search_contact_bday(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The search_contact_bday function searches for contacts with birthdays in the next 7 days.
        Args:
            db (AsyncSession): The database session to use. Defaults to Depends(get_db).
            current_user (User): The user making the request. Defaults to Depends(auth_service.get_current_user).

    :param db: AsyncSession: Get the database session
    :param current_user: User: Get the current user from the auth_service
    :param : Get the current user
    :return: A list of contacts that have a birthday in the next 7 days
    """
    contact = await repositories_contacts.search_contacts_bday(current_user, db, days=7)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ITEM_NOT_FOUND
        )
    return contact
