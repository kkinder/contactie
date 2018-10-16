"""
Just serves the index.html file, because I can't figure out why whitenoise won't do it right now.
"""

# TODO: This is whitenoise's job.

import os


class IndexResource(object):
    def on_get(self, req, resp):
        resp.body = open(os.path.join(STATIC_CONTENT_DIR, 'index.html')).read()
        resp.content_type = 'text/html'


from api_server import STATIC_CONTENT_DIR
