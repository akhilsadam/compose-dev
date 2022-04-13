"""Routes for Flask app."""
import os
from flask import current_app as app

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_apispec.extension import FlaskApiSpec


from marshmallow import Schema, fields



appname = "hw05"
apiversion='v0.0.1'

app.config.update({
    'APISPEC_SPEC': APISpec(
        title=appname,
        version=apiversion,
        openapi_version="3.0.2",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/api',
    'APISPEC_SWAGGER_UI_URL': '/api/doc',
})
docs = FlaskApiSpec(app)

denylist = ['__pyc','__init']

for file in os.listdir('app/api/'):
    if all(item not in file for item in denylist):
        page = file[:len(file)-3]
        print(page)
        exec(f'from app.api.{page} import {page}')
        #exec(f'docs.register({page})')
    # exec(f'app.register_blueprint({page})')