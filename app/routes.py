"""Routes for Flask app."""
import os

from flask import Blueprint, current_app as app, request as rq
from flask import render_template
import requests as rqs

from app.options import options

import logging
logger = logging.getLogger('root')

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_apispec.extension import FlaskApiSpec
from functools import lru_cache
from app.schema import * #schema

@app.route("/", methods=['GET'])
def home():
    """Application homepage.
    ---
    get:
      description: Get homepage HTML
      security:
        - ApiKeyAuth: []
      responses:
        200:
          description: Return homepage HTML
          content:
            application/json:
              schema: HTML
    """
    return render_template(
        "main.jinja2",
        title=options.appname,
        description="",
        template="home-template",
        proxy=options.proxy,
        readmelink = options.readmelink,
        apilink = "/api"
    )

@app.route("/api/doc", methods=['GET'])
def api():
    """Application API, styled.
    ---
    get:
      description: Get API HTML
      security:
        - ApiKeyAuth: []
      responses:
        200:
          description: Return API HTML
          content:
            application/json:
              schema: HTML
    """
    # with open("app/static/dist/css/styleapi.css",'r') as f:
    #     css = f.read().replace("\n"," ")
    return render_template(
        "api.jinja2",
        title=options.appname,
        description="",
        template="home-template",
        readmelink = options.readmelink,
        proxy=options.proxy,
        apilink = "/api",
    )

@app.route("/pdf", methods=['GET'])
def pdf():
    """Application writeup / research article.
    ---
    get:
      description: Get writeup HTML
      security:
        - ApiKeyAuth: []
      responses:
        200:
          description: Return writeup HTML
          content:
            application/json:
              schema: HTML
    """
    return render_template(
        "readme.jinja2",
        proxy=options.proxy,
        general="",
        template="home-template",
    )

@lru_cache(maxsize=1)
def proxyAPI():
    """One-time function to get, update, and return links in API html
    Returns:
        str: replaced HTML
    """
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/html',
    }
    htm = rqs.get(f"{options.getURL()}/api/local",headers=headers).text
    return htm.replace("/flask-apispec",f"{options.proxy}/flask-apispec").replace("<title>Swagger UI</title>","<title>Proxy-Modified Swagger UI</title>")

@app.route("/api", methods=['GET'])
def swagger() -> str:
    """
    Application api (Swagger Proxy workaround)
    ---
    get:
      description: Get API as HTML page
      security:
        - ApiKeyAuth: []
      responses:
        200:
          description: Return API HTML
          content:
            application/json:
              schema: HTML
    """
    try: 
        return proxyAPI()
    except Exception as E:
        return f"API Generation Failed with exception {E}"

app.config.update({
    'APISPEC_SPEC': APISpec(
        title=options.appname,
        version=options.apiversion,
        openapi_version="3.0.2",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/api/api.json',
    'APISPEC_SWAGGER_UI_URL': '/api/local'
})

docs = FlaskApiSpec(app)

docs.register(home)
docs.register(pdf)
docs.register(api)
docs.register(swagger)
### EVENT REGISTRATION | PLEASE LINE UP BY CLASS ###

denylist = ['__pyc','__init','test','schema']
denymethodlist = ['as_view','dispatch_request']

methods = []
for file in os.listdir('app/api/'):
    if all(item not in file for item in denylist):
        page = file[:len(file)-3]
        exec(f'from app.api.{page} import {page}')
        exec(f"methods = [attribute for attribute in dir({page}) if callable(getattr({page}, attribute)) and not attribute.startswith('__') and attribute not in denymethodlist]")
        for method in methods:
            logger.debug(f'{method}')
            # print(method)
            exec(f'docs.register({page}.{method})')
    # exec(f'app.register_blueprint({page})')

#------------------------------------------------------ 
# from app.queue.worker import worker
# import threading
# # make 2 new workers and start them
# def work():
#   worker().execute_job()
# for _ in range(2):
#   threading.Thread(target=work, args=(), kwargs={}).start()

#------------------------------------------------------ 
from app.api.piece import piece
piece.init() # initialize app
