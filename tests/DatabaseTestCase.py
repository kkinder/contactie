import os
import sys
import unittest

import dotenv
import sqlalchemy
from faker import Faker

import db.models as m
from db import configure_session, Session

# .env-test in this file's path
DEFAULT_TEST_ENVIRONMENT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.env-test')

dotenv.load_dotenv(os.environ.get('TEST_ENVIRONMENT', DEFAULT_TEST_ENVIRONMENT))

assert sys.version_info.major >= 3, "We don't use Python 2"


class TestingEnvironmentError(Exception):
    pass


class DatabaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.database_url = os.environ.get('DATABASE_URL', '').strip()
        if not cls.database_url:
            raise TestingEnvironmentError('No DATABASE_URL defined')

        print('Using database: %s' % cls.database_url)

        configure_session(database_url=cls.database_url)
        session = Session()

        # Enable uuid extension, which isn't enabled by default.
        session.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
        session.commit()

    def setUp(self):
        self.session = Session()
        sqlalchemy.orm.configure_mappers()
        m.metadata.create_all(bind=self.session.bind)
        self.fake = Faker()

    def tearDown(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
