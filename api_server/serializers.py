from db import models as m


def serialize_contact(contact: m.Contact):
    """
    Generates a suitable document for resp.media.

    DOES NOT handle HTTP status setting.

    :param contact: Contact Object
    :param resp: Falcon response object
    """
    assert contact.id, 'Session should be flushed'

    return {
        'id': str(contact.id),
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'date_of_birth': contact.date_of_birth.isoformat(),
        'email_addresses': contact.emails,
        'phone_numbers': contact.phone_numbers,
        'addresses': contact.addresses,
    }
