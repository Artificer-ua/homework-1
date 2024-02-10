from datetime import date, timedelta

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession, current_user: User):
    """
    The get_contacts function returns a list of contacts for the current user.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the offset of the first row to return
    :param db: AsyncSession: Pass in the database session object
    :param current_user: User: Filter the contacts by user
    :return: A list of contact objects
    """
    stmt = (
        select(Contact)
        .filter_by(user_id=int(current_user.id))
        .offset(offset)
        .limit(limit)
    )
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, current_user: User):
    """
    The get_contact function is used to retrieve a single contact from the database.
    It takes in an integer representing the id of the contact, and returns a Contact object.


    :param contact_id: int: Specify the id of the contact to be retrieved
    :param db: AsyncSession: Pass in the database session to use
    :param current_user: User: Check that the user is authorized to access this contact
    :return: A contact object or none
    """
    stmt = select(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == current_user.id)
    )
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession, current_user):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactSchema: Validate the data that is passed in
    :param db: AsyncSession: Pass in the database session
    :param current_user: Get the user_id from the current logged in user
    :return: A contact object
    """
    contact = Contact(**body.model_dump(exclude_unset=True), user_id=current_user.id)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(
    contact_id: int, body: ContactSchema, db: AsyncSession, current_user
):
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactSchema): A ContactSchema object containing all fields for a new Contact object.

    :param contact_id: int: Specify the contact id of the contact we want to update
    :param body: ContactSchema: Pass the data from the request body into this function
    :param db: AsyncSession: Pass the database connection to the function
    :param current_user: Check if the user is authorized to update a contact
    :return: A contact object
    """
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
    """
    The delete_contact function deletes a contact from the database.

    :param contact_id: int: Specify which contact to delete
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: Ensure that the user is only deleting their own contacts
    :return: The deleted contact
    """
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
    """
    The search_contacts_bday function searches for contacts with birthdays within a given number of days.
        Args:
            current_user (User): The user who is currently logged in.
            db (AsyncSession): An async session to the database.
            days (int): The number of days from today to search for birthdays in.

    :param current_user: User: Filter the contacts by user_id
    :param db: AsyncSession: Pass the database session to the function
    :param days: Determine how many days in the future we want to search for birthdays
    :return: A list of contacts with birthdays in the next x days
    """
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
    """
    The search_contact function takes in a search string, an async database session, and the current user.
    It then creates a SQLAlchemy statement that searches for contacts with firstname, lastname or email matching the search string.
    The function returns all of these contacts.

    :param search_string: str: Search for a string in the database
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: User: Filter the results to only show contacts that belong to the current user
    :return: A list of contacts that match the search string
    """
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
