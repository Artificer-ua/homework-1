import sys
from datetime import date, timedelta
from os.path import abspath, dirname, join

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

# sys.path.insert(0, abspath(join(dirname(__file__), "..")))

from src.entity.models import Contact
from src.schemas.contact import ContactSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone = body.phone
        contact.bday = body.bday
        contact.notes = body.notes
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contacts_bday(db: AsyncSession, days):
    date_from = date.today()
    date_to = date.today() + timedelta(days=days)
    this_year = date_from.year
    stmt = select(Contact).filter(
        func.to_date(
            func.concat(func.to_char(Contact.bday, "DDMM"), this_year), "DDMMYYY"
        ).between(date_from, date_to)
    )
    contact = await db.execute(stmt)
    return contact.scalars().all()


async def search_contact(search_string: str, db: AsyncSession):
    search = "%{}%".format(search_string)
    stmt = select(Contact).filter(
        or_(
            Contact.firstname.ilike(search),
            Contact.lastname.ilike(search),
            Contact.email.ilike(search),
        )
    )
    contact = await db.execute(stmt)
    return contact.scalars().all()
