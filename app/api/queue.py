import os
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
from app.shaft import access

class queue:

  @app.route("/queue/", methods=['GET'])
  def list_queue() -> str:
      """ Return a list of all waiting jobs...
      ---
      get:
        description: Get job data from Redis.
        security:
          - ApiKeyAuth: []
        parameters:
        - name: start
          in: path
          description: Job Index (int) in time to start from for the data list.
          required: false
          example: 0
        responses:
          200:
            description: Return all queued job data as JSON
            content:
              application/json:
                schema: JSON            
      """
      a0 = rq.args.get('start', 0)
      route = '/queue/'
      try: st = int(a0)
      except ValueError: 
          msg = "Invalid start parameter. Please input an integer"
          logger.error(f'{route}:{msg}')
          return msg
      # logger.info(f"GET : {route}")
      out = access.redis_hget(1)
      out.sort(key=lambda x: x['id'],reverse=True)
      if st != 0:
        out = out[:-st]
      response =  jsonify(out)
      return response


          