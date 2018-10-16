"""
Server file.
"""
import os
from wsgiref import simple_server

import dotenv

from api_server import get_app
from db import configure_session

dotenv.load_dotenv()

configure_session(database_url=os.environ['DATABASE_URL'])
app = get_app()



if __name__ == '__main__':
    print('Serving on port 8000...')
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
