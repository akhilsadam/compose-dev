"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment, Bundle
import sys
import app.options

### ReverseProxy for Kubernetes

class ReverseProxied(object):
    def __init__(self, app, script_name):
        """proxy init

        Args:
            app (flaskapp): the un-proxied app
            script_name (str): the proxy directory
        """
        self.app = app
        self.script_name = script_name

    def __call__(self, environ, start_response):
        """function for passing callbacks

        Args:
            environ (dict): proxy environment
            start_response (object): start_response object

        Returns:
            flaskapp: flask application
        """
        environ['SCRIPT_NAME'] = self.script_name
        return self.app(environ, start_response)

###



ipa = sys.argv[1]
app.options.options.sethost(ipa)

import logging
logger = logging.getLogger('root')

from app import init_app
"""Application entry point."""
if __name__ == "__main__":
    app = init_app()

    # setup reverse proxy if on kubernetes
    try: proxy = sys.argv[2]
    except:
        pass
    else:
        app.wsgi_app = ReverseProxied(app.wsgi_app, script_name=f'/{proxy}')

    port = 5026
    app.run(host="0.0.0.0", debug=False,port=port)
