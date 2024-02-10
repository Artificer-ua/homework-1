import os
import sys
import unittest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

sys.path.append(os.path.abspath(".."))

from src.entity.models import Contact, User
from src.repository.contacts import (
    create_contact,
    delete_contact,
    get_contact,
    get_contacts,
    search_contact,
    update_contact,
)
from src.schemas.contact import ContactSchema


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(id=1, username="TestUser", password="12345678", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [
            Contact(
                id=1,
                firstname="Name1",
                lastname="Surname1",
                email="1example@mail.com",
                phone="0671234567",
                bday=datetime.strptime("2000-01-19", "%Y-%m-%d").date(),
                notes="",
                user_id=self.user,
            ),
            Contact(
                id=2,
                firstname="Name2",
                lastname="Surname2",
                email="2example@mail.com",
                phone="0631234567",
                bday=datetime.strptime("1999-01-19", "%Y-%m-%d").date(),
                notes="",
                user_id=self.user,
            ),
        ]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(
            limit=limit, offset=offset, db=self.session, current_user=self.user
        )
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        test_contact = Contact(
            id=2,
            firstname="Name1",
            lastname="Surname1",
            email="1example@mail.com",
            phone="0671234567",
            bday=datetime.strptime("2000-01-19", "%Y-%m-%d").date(),
            notes="",
            user_id=self.user,
        )
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = test_contact

        self.session.execute.return_value = mocked_contact
        result = await get_contact(
            contact_id=2, db=self.session, current_user=self.user
        )
        self.assertEqual(result, test_contact)

    async def test_create_contact(self):
        body = ContactSchema(
            firstname="FirstName",
            lastname="LastName",
            email="test@example.com",
            phone="1234567",
            bday=datetime.strptime("2000-01-19", "%Y-%m-%d").date(),
            notes="",
        )
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.firstname, body.firstname)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.email, body.email)

    async def test_update_contact(self):
        body = ContactSchema(
            firstname="FirstName",
            lastname="LastName",
            email="test@example.com",
            phone="1234567",
            bday=datetime.strptime("2000-01-19", "%Y-%m-%d").date(),
            notes="",
        )
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(
            firstname="Nameqq",
            lastname="Nameeee",
            email="test@example.com",
            phone="123",
            bday=datetime.strptime("2000-01-19", "%Y-%m-%d").date(),
            notes=None,
        )
        self.session.execute.return_value = mocked_contact

        result = await update_contact(1, body, self.session, self.user)

        self.assertIsInstance(result, Contact)
        self.assertEqual(result.firstname, body.firstname)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.email, body.email)

    async def test_delete_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(
            id=1,
            firstname="Nameqq",
            lastname="Nameeee",
            email="test@example.com",
            phone="123",
            bday=datetime.strptime("2000-01-19", "%Y-%m-%d").date(),
            notes=None,
        )
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(1, self.session, self.user)
        # if del method was called
        self.session.delete.assert_called_once()
        # if commit method was called
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, Contact)

    async def test_search_contact(self):
        contacts = [
            Contact(
                id=2,
                firstname="Name1",
                lastname="Surname1",
                email="1example@mail.com",
                phone="0671234567",
                bday=datetime.strptime("2000-01-19", "%Y-%m-%d").date(),
                notes="",
                user_id=self.user,
            ),
            Contact(
                id=3,
                firstname="Name2",
                lastname="Surname2",
                email="2example@gmail.com",
                phone="0631234567",
                bday=datetime.strptime("1999-01-19", "%Y-%m-%d").date(),
                notes="",
                user_id=self.user,
            ),
        ]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts

        self.session.execute.return_value = mocked_contacts

        result = await search_contact(
            search_string="Test", db=self.session, current_user=self.user
        )
        self.assertEqual(result, contacts)
        self.assertEqual(result[0].firstname, "Name1")


if __name__ == "__main__":
    unittest.main()
