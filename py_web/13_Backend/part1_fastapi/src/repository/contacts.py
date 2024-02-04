from datetime import date, timedelta

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..entity.models import Contact, User
from ..schemas.contact import ContactSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession, current_user: User):
    stmt = (
        select(Contact)
        .filter_by(user_id=int(current_user.id))
        .offset(offset)
        .limit(limit)
    )
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, current_user: User):
    stmt = select(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == current_user.id)
    )
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession, current_user):
    contact = Contact(**body.model_dump(exclude_unset=True), user_id=current_user.id)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(
    contact_id: int, body: ContactSchema, db: AsyncSession, current_user
):
    stmt = select(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == current_user.id)
    )
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone = body.phone
        contact.bday = body.bday
        contact.notes = body.notes
        contact.user_id = current_user.id
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, current_user):
    stmt = select(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == current_user.id)
    )
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contacts_bday(current_user: User, db: AsyncSession, days):
    date_from = date.today()
    date_to = date.today() + timedelta(days=days)
    this_year = date_from.year
    stmt = select(Contact).filter(
        and_(
            (
                func.to_date(
                    func.concat(func.to_char(Contact.bday, "DDMM"), this_year),
                    "DDMMYYY",
                ).between(date_from, date_to)
            ),
            Contact.user_id == current_user.id,
        )
    )
    contact = await db.execute(stmt)
    return contact.scalars().all()


async def search_contact(search_string: str, db: AsyncSession, current_user: User):
    search = "%{}%".format(search_string)
    stmt = select(Contact).filter(
        and_(
            or_(
                Contact.firstname.ilike(search),
                Contact.lastname.ilike(search),
                Contact.email.ilike(search),
            )
        ),
        Contact.user_id == current_user.id,
    )
    contact = await db.execute(stmt)
    return contact.scalars().all()
