# import sys
# from os.path import abspath, dirname, join

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

# sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from src.database.connect import get_db
from src.entity.models import User
from src.repository import contacts as repositories_contacts
from src.schemas.contact import ContactResponse, ContactSchema
from src.services.auth import auth_service

router_contact = APIRouter(prefix='/contacts', tags=['contacts'])



@router_contact.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                    db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repositories_contacts.get_contacts(limit, offset, db, current_user)
    return contacts


@router_contact.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return contact


@router_contact.post("/{contact_id}", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.create_contact(body, db, current_user)
    return contact


@router_contact.put("/{contact_id}")
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return contact


@router_contact.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.delete_contact(contact_id, db, current_user)
    return contact


@router_contact.get("/search/{search_string}", response_model=list[ContactResponse])
async def search_contact(search_string: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.search_contact(search_string, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return contact



@router_contact.get("/search/", response_model=list[ContactResponse])
async def search_contact_bday(db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.search_contacts_bday(current_user, db, days=7)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Items not found")
    return contact

