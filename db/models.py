from sqlalchemy import Column, DateTime, Date, ForeignKey, String, text, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils import TSVectorType

Base = declarative_base()
metadata = Base.metadata

make_searchable(metadata=metadata)


class Contact(Base):
    __tablename__ = 'contact'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))

    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)

    created = Column(DateTime, nullable=False, server_default=text("now()"))

    # 0 or more
    addresses = Column(ARRAY(String))

    # 1 or more, but validate in controller
    emails = Column(ARRAY(String))
    phone_numbers = Column(ARRAY(String))

    search_vector = Column(TSVectorType('first_name', 'last_name'))
