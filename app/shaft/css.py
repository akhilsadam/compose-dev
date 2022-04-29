import os
from app.options import options
import logging
logger = logging.getLogger('root')

def css_replace(proxy):
    """Edit css files to fix urls for proxy.

    Args:
        proxy (str): proxy url header
    """
    path = f'/app/app/static/dist/css/'
    for file in os.listdir(path):
        with open(path+file,'r') as f:
            data = f.read()
        data=data.replace('url("/static',f'url("{proxy}/static')
        with open(path+file,'w') as f:
            f.write(data)
    logger.info("Fixed CSS.")
