"""
Queries contacts.
"""

import falcon
from sqlalchemy_searchable import search

from api_server.serializers import serialize_contact
from db import session_scope, models as m


class ContactQueryResource:
    # TODO: Pagination

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        search_terms = req.params.get('q', '').strip()

        with session_scope() as session:
            query = session.query(m.Contact)

            if search_terms:
                query = search(query, search_terms, sort=True)
            else:
                query = query.order_by(m.Contact.last_name, m.Contact.first_name)

            contacts = [serialize_contact(contact=contact) for contact in query]

            resp.media = {
                'contacts': contacts,
                'count': len(contacts)
            }
            resp.status = falcon.HTTP_200
