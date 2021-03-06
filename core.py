"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment, Bundle
import sys
import app.options


ipa = sys.argv[1]
app.options.options.sethost(ipa)

import app.log as log
logger = log.init_logger('root')

# # setup reverse proxy if on kubernetes
logger.info("Checking for Proxy...")
try: proxy = sys.argv[2]
except:
    logger.info("Proxy not found.")
else:
    logger.info(f"Found Proxy : {proxy}")
    app.options.options.setproxy(proxy)

from app import init_app
"""Application entry point."""
if __name__ == "__main__":
    app = init_app()
    port = 5026
    app.run(host="0.0.0.0", debug=False,port=port)
