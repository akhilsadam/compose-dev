import os

from itsdangerous import base64_encode

import redis
from flask import Blueprint, jsonify, render_template
from flask import current_app as app
from flask import request as rq
import requests as rqs
import json as js

from flask_apispec import MethodResource, use_kwargs, marshal_with
from marshmallow import Schema
from webargs import fields

import logging
logger = logging.getLogger('root')

from app.options import options
from app.schema import *

from app.queue.jobs import jobs
from app.redisclient import redis_client_raw
# IMPORTANT: make sure to name the class you use the same as the filename!
# IMPORTANT: any non-route methods should not be in the class!
class analyze(MethodResource):

    @app.route("/analyze/value/<int:songid>/", methods=['GET'])
    def value_single(songid : int) -> str:
        """ Return emotional value (eV) information for piece as plot
        ---
        get:
          description: Get eV data from Redis.
          security:
            - ApiKeyAuth: []
          parameters:
          - name: songid
            in: path
            description: Index (int) select from for the data list.
            required: true
            example: 0
          responses:
            200:
              description: Return a single piece's eV plot as HTML
              content:
                application/json:
                  schema: HTML            
        """
        route = f'/analyze/value/{songid}/'
        resp = redis_client_raw(7).get(f'{songid}_0')
        if resp is None:
            jobs.job(["appfields", "create_eV_plots", songid]) # add job to queue with class name and method and args.
            msg = "No plot available yet; A job was submitted. Please wait a few moments and try again ... \
              If you have done so, then no such piece exists. Check route /piece for all pieces. \
              Check route /queue for job information."
            logger.error(f'{route}:{msg} - redis client did not find image...')
            return msg
        # logger.info(f"GET : {route}")
        byte = resp.decode("utf-8").replace("\n", "")
        return render_template(
          "img.jinja2",
          img=byte,
          # img=resp,
        )

        