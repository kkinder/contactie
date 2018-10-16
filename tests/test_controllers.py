import unittest

import falcon.testing

import db.models as m
from api_server import get_app
from tests.DatabaseTestCase import DatabaseTestCase


class TestControllers(DatabaseTestCase, falcon.testing.TestCase):
    def __init__(self, *args, **kwargs):
        # Multiple inheritance joy
        DatabaseTestCase.__init__(self, *args, **kwargs)
        falcon.testing.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        DatabaseTestCase.setUp(self)
        falcon.testing.TestCase.setUp(self)

        self.app = get_app()

        # Wipe out any existing test data. Ideally, the test database is fresh, but this is quick/lazy for demo.
        self.session.query(m.Contact).delete()
        self.session.commit()

    def test_create_contact(self):
        """
        Creates a contact and spot checks it in the database
        """
        result, request_doc = self._create_contact()

        self.assertEqual(result.status_code, 201)
        contact_id = result.json['id']
        self.assert_(contact_id)

        contact = self.session.query(m.Contact).get(contact_id)
        # Spot check a few fields...
        self.assertEqual(contact.first_name, request_doc['first_name'])
        self.assertEqual(contact.emails, request_doc['email_addresses'])
        self.assertEqual(contact.addresses, request_doc['addresses'])

    def test_get_contact(self):
        result, doc = self._create_contact()

        serialized_result_from_create = result.json

        result = self.simulate_get('/api/contact/{}'.format(result.json['id']))
        self.assertEqual(result.status_code, 200)
        serialized_result_from_get = result.json

        # They should be the same.
        self.assertEqual(serialized_result_from_create, serialized_result_from_get)

    def test_delete_contact(self):
        result, doc_from_create = self._create_contact()
        contact_id = result.json['id']

        result = self.simulate_delete('/api/contact/{}'.format(contact_id))
        self.assertEqual(result.status_code, 200)

        self.assertEqual(self.session.query(m.Contact).get(contact_id), None)

    def test_query_contact(self):
        # Create 3 contacts
        names = [('Homer', 'Simpson'), ('Lisa', 'Simpson'), ('Edna', 'Krabappel')]
        for first, last in names:
            result, doc_from_create = self._create_contact(first, last)

        result = self.simulate_get('/api/contact')
        self.assertEqual(result.status_code, 200)
        doc = result.json

        # Edna should be first
        self.assertEqual(doc['contacts'][0]['first_name'], 'Edna')

        # 3 docs
        self.assertEqual(doc['count'], 3)

        result = self.simulate_get('/api/contact', params={'q': 'Simpson'})
        doc = result.json
        self.assertEqual(doc['count'], 2)


    def test_update_contact(self):
        result, doc_from_create = self._create_contact()

        result = self.simulate_get('/api/contact/{}'.format(result.json['id']))
        doc = result.json

        new_name = self.fake.first_name()
        doc['first_name'] = new_name

        result = self.simulate_post('/api/contact/{}'.format(doc['id']), json=doc)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['first_name'], new_name)

    def _create_contact(self, first_name=None, last_name=None):
        if not first_name:
            first_name = self.fake.first_name()
        if not last_name:
            last_name = self.fake.last_name()
        date_of_birth = self.fake.date()
        phone_number = self.fake.phone_number()
        email = self.fake.email()
        address = self.fake.address()
        request_doc = {
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth,
            'phone_numbers': [phone_number],
            'email_addresses': [email],
            'addresses': [address],
        }
        result = self.simulate_post('/api/contact/_new', json=request_doc)
        return result, request_doc


if __name__ == '__main__':
    unittest.main()
