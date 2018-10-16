"""
Falcon CRUD server
"""
import os
import pathlib

import falcon
from whitenoise import WhiteNoise


APP_DIR = pathlib.Path(__file__).parent.absolute()
STATIC_CONTENT_DIR = str((pathlib.Path(APP_DIR) / '..' / 'webapp-dist').absolute())

#assert os.path.exists(STATIC_CONTENT_DIR)


def add_whitenoise(app):
    app = WhiteNoise(app, root=STATIC_CONTENT_DIR)
    app.index_file = 'index.html'
    return app


def get_app():
    from api_server.ContactQueryResource import ContactQueryResource
    from api_server.ContactResource import ContactResource
    from api_server.IndexResource import IndexResource

    falcon_app = falcon.API()

    # This is safe because 'query' will never be an ID.
    falcon_app.add_route('/', IndexResource())
    falcon_app.add_route('/api/contact', ContactQueryResource())
    falcon_app.add_route('/api/contact/{contact_id}', ContactResource())

    falcon_app = add_whitenoise(falcon_app)

    return falcon_app
