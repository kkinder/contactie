"""
Controller for CRUD on contacts.
"""
from datetime import datetime

import falcon
import jsonschema

from api_server.serializers import serialize_contact
from db import session_scope, models as m


def parse_date(value):
    RFC3339_STRING = '%Y-%m-%dT%H:%M:%S.%fZ'
    RFC3339_NO_FRACTION = '%Y-%m-%dT%H:%M:%SZ'
    RFC3339_NO_ZULU = '%Y-%m-%dT%H:%M:%S.%f'
    RFC3339_NO_FRACTION_NO_ZULU = '%Y-%m-%dT%H:%M:%S'
    BASIC_ISO = '%Y-%m-%d'

    VALID_DATETIME_STRINGS = [
        RFC3339_STRING, RFC3339_NO_FRACTION, RFC3339_NO_ZULU, RFC3339_NO_FRACTION_NO_ZULU, BASIC_ISO
    ]

    for format_string in VALID_DATETIME_STRINGS:
        try:
            return datetime.strptime(value, format_string)
        except ValueError:
            pass

    raise falcon.HTTPBadRequest('Bad request', 'Invalid date format: %r' % (value,))


class ContactResource:
    """
    CRUD for Contact. Query is ContactQueryResource.py
    """
    contact_schema = {
        'title': 'contact',
        'type': 'object',
        'properties': {
            'id': {'type': 'string'},
            'first_name': {'type': 'string'},
            'last_name': {'type': 'string'},
            'date_of_birth': {'type': 'string', 'format': 'date-time'},
            'addresses': {'items': {'type': 'string'}, 'type': 'array'},
            'phone_numbers': {
                'type': 'array',
                'items': {'type': 'string'},
                'min_items': 1
            },
            'email_addresses': {
                'type': 'array',
                'items': {'type': 'string'},
                'min_items': 1
            },
        },
        'additionalProperties': False,
        'required': ['first_name', 'last_name', 'date_of_birth', 'addresses', 'phone_numbers', 'email_addresses']
    }

    def on_get(self, req: falcon.Request, resp: falcon.Response, contact_id):
        with session_scope() as session:
            contact = session.query(m.Contact).get(contact_id)
            if not contact:
                raise falcon.HTTPNotFound()

            resp.media = serialize_contact(contact=contact)
            resp.status = falcon.HTTP_200

    def on_post(self, req: falcon.Request, resp: falcon.Response, contact_id):
        doc = self._validate_input(req=req, schema=self.contact_schema, generate_falcon_errors=True)

        with session_scope() as session:
            # Get the contact, or create a new one
            if contact_id == '_new':
                contact = m.Contact()
                session.add(contact)
            else:
                contact = session.query(m.Contact).get(contact_id)
                if not contact:
                    raise falcon.HTTPNotFound()

            # Update the contact
            self._update_contact(contact, doc)

            # Serialize the output and set the relevant HTTP status.
            session.flush()
            resp.media = serialize_contact(contact=contact)
            if contact_id == '_new':
                resp.status = falcon.HTTP_201  # Created
            else:
                resp.status = falcon.HTTP_200  # Updated

    def on_delete(self, req: falcon.Request, resp: falcon.Response, contact_id):
        with session_scope() as session:
            # Get the contact, or create a new one
            contact = session.query(m.Contact).get(contact_id)
            if not contact:
                raise falcon.HTTPNotFound()

            session.delete(contact)
            resp.status = falcon.HTTP_200  # Updated

    def _validate_input(self, req: falcon.Request, schema=None, generate_falcon_errors=True):
        """
        Used to decode JSON requests.

        :param req: Falcon request
        :param schema: JSON Schema, if any
        :param generate_falcon_errors: If True, will generate HTTP Error if input doesn't match schema
        :return: Decoded document
        """
        if req.content_length:
            doc = req.media
            if schema:
                try:
                    jsonschema.validate(doc, schema=schema)
                except jsonschema.ValidationError as e:
                    if generate_falcon_errors:
                        raise falcon.HTTPBadRequest('Bad request', e.message)
                    else:
                        raise

            # Do some extra validation
            for (key_name, message) in (('phone_numbers', 'Must specify at least one phone number'),
                                        ('email_addresses', 'Must specify at least one email address')):
                doc[key_name] = [n.strip() for n in doc[key_name]]

                while '' in doc[key_name]:
                    doc[key_name].remove('')

                if not doc[key_name]:
                    raise falcon.HTTPBadRequest('Bad request', message)

            # Validate email addresses
            for email_address in doc['email_addresses']:
                if '@' not in email_address:
                    raise falcon.HTTPBadRequest('Bad request', 'Invalid email address: {}'.format(email_address))

            return doc
        else:
            if generate_falcon_errors:
                raise falcon.HTTPBadRequest('Bad request', 'No JSON document posted')

    def _update_contact(self, contact: m.Contact, doc):
        """
        Updates the Contact object according to what's in the doc.

        :param contact: Contact object
        :param doc: Dictionary with values defined by schema.
        """

        # NOTE: I would probably prefer some kind of standard serializer/deserializer, but this works for a simple
        # example.
        contact.first_name = doc['first_name']
        contact.last_name = doc['last_name']
        contact.date_of_birth = parse_date(doc['date_of_birth']).date()
        contact.emails = doc['email_addresses']
        contact.phone_numbers = doc['phone_numbers']
        contact.addresses = doc['addresses']
