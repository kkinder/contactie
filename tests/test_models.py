import unittest

import db.models as m
from tests.DatabaseTestCase import DatabaseTestCase


class TestModels(DatabaseTestCase):
    def test_create_contact(self):
        contact = self._create_full_contact()
        self.session.commit()

        # Just make sure round trip happened
        self.assertEqual(self.session.query(m.Contact).get(contact.id), contact)
        self.assertEqual(len(self.session.query(m.Contact).get(contact.id).phone_numbers), 3)

    def _create_full_contact(self, addresses_count=3, phone_numbers_count=3, email_addresses_count=3):
        # Create a contact
        contact = m.Contact(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            date_of_birth=self.fake.date(),
            addresses=[self.fake.address() for i in range(addresses_count)],
            emails=[self.fake.email() for i in range(email_addresses_count)],
            phone_numbers=[self.fake.phone_number() for i in range(phone_numbers_count)],
        )
        self.session.add(contact)

        return contact


if __name__ == '__main__':
    unittest.main()
