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

import redis

def redis_client():
    """Get Redis Client.

    Returns:
        object: redis server object.
    """
    print(f"REDIS host IP: {options.redhost}")
    return redis.Redis(host=options.redhost, port=options.redport, db=0, charset="utf-8", decode_responses=True)

mainkey='meteorite_landings'

class data(MethodResource):

    loaded = False      

    @app.route("/data", methods=['POST'])
    def data_in():
        """Get Meteorite Landing observations from website to Redis.
        """
        try:
            dt = js.loads(rqs.get("https://raw.githubusercontent.com/wjallen/coe332-sample-data/main/ML_Data_Sample.json")
                .content.decode('utf-8'))[mainkey]
            rd = redis_client()
            for i in range(len(dt)):
                rd.hset(i,mapping=dt[i])
            data.loaded = True
        except Exception as E:
            logger.critical(E)
        else:
            return "Successful Load!"

    def data():
        """Get Meteorite Landing observations from Redis
            Returns:
                list: a list of dictionaries contain ML data.
        """
        if data.loaded == False:
            data.data_in()
        rd = redis_client()
        return [rd.hgetall(key) for key in rd.keys()]

    @app.route("/data", methods=['GET'])
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
			  description: Return Meteorite Landing data as json.
			  content:
				application/json
        post:
          description: Get Meteorite Landing data from Redis.
          security:
            - ApiKeyAuth: []
          responses:
            201:
                description: Updated Redis database.
        """
        a0 = rq.args.get('start', 0)
        route = '/degrees'
        try: st = int(a0)
        except ValueError: 
            msg = "Invalid start parameter. Please input an integer"
            logger.error(f'{route}:{msg}')
            return msg
        # logger.info(f"GET : {route}")
        out = data.data()[st:]
        print(out)
        return jsonify(out)

        