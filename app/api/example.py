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
from app.api.schema import *

from app.redisclient import redis_client
mainkey='meteorite_landings'

def data_out():
    """Get Meteorite Landing observations from Redis
        Returns:
            list: a list of dictionaries contain ML data.
    """
    if example.loaded == False:
        example.data_in()
    rd = redis_client(15)
    return [rd.hgetall(key) for key in rd.keys()]

# IMPORTANT: make sure to name the class you use the same as the filename!
# IMPORTANT: any non-route methods should not be in the class!
class example(MethodResource):

    loaded = False      

    @app.route("/example", methods=['POST'])
    def data_in():
        """Get Meteorite Landing observations from website to Redis.
        ---
        post:
          description: Get Meteorite Landing data from Redis.
          security:
            - ApiKeyAuth: []
          responses:
            201:
              description: Update Redis database 
        """
        try:
            dt = js.loads(rqs.get("https://raw.githubusercontent.com/wjallen/coe332-sample-data/main/ML_Data_Sample.json")
                .content.decode('utf-8'))[mainkey]
            rd = redis_client(15)
            for i in range(len(dt)):
                rd.hset(i,mapping=dt[i])
            example.loaded = True
        except Exception as E:
            logger.critical(E)
        else:
            return "Successful Load!"

    @app.route("/example", methods=['GET'])
    def data_io():
        """ Meteorite Landing observations
        ---
        get:
          description: Get Meteorite Landing data from Redis.
          security:
            - ApiKeyAuth: []
          parameters:
          - name: start
            in: path
            description: Index (int) to start from for the data list.
            required: false
            example: 0
          responses:
            200:
              description: Return API HTML
              content:
                application/json:
                  schema: HTML            
        """
        a0 = rq.args.get('start', 0)
        route = '/degrees'
        try: st = int(a0)
        except ValueError: 
            msg = "Invalid start parameter. Please input an integer"
            logger.error(f'{route}:{msg}')
            return msg
        # logger.info(f"GET : {route}")
        out = data_out()[st:]
        print(out)
        return jsonify(out)

        