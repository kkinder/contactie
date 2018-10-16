"""
Falcon CRUD server
"""
import pathlib

import falcon
import whitenoise

APP_DIR = pathlib.Path(__file__).parent.absolute()
STATIC_CONTENT_DIR = str((pathlib.Path(APP_DIR) / '..' / 'webapp-dist').absolute())


class StaticApp(whitenoise.WhiteNoise):
    def __call__(self, environ, start_response):
        path = whitenoise.base.decode_path_info(environ['PATH_INFO'])

        static_file = self._get_file(path)

        if static_file is None and not path.startswith('/api/'):
            static_file = self._get_file('/index.html')
            return self.serve(static_file, environ, start_response)
        elif static_file is None:
            return self.application(environ, start_response)
        else:
            return self.serve(static_file, environ, start_response)

    def _get_file(self, path):
        static_file = self.files.get(path)
        return static_file


def add_whitenoise(app):
    app = StaticApp(app, root=STATIC_CONTENT_DIR)
    app.index_file = 'index.html'
    return app


def get_app():
    from api_server.ContactQueryResource import ContactQueryResource
    from api_server.ContactResource import ContactResource

    falcon_app = falcon.API()

    # This is safe because 'query' will never be an ID.
    falcon_app.add_route('/api/contact', ContactQueryResource())
    falcon_app.add_route('/api/contact/{contact_id}', ContactResource())

    falcon_app = add_whitenoise(falcon_app)

    return falcon_app
