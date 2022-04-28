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
# IMPORTANT: make sure to name the class you use the same as the filename!
# IMPORTANT: any non-route methods should not be in the class!
class piece(MethodResource):

    loaded = False      

    @app.route("/init", methods=['POST'])
    def init():
        """Set up all example pieces in repository
        ---
        post:
          description: Create examples.
          security:
            - ApiKeyAuth: []
          responses:
            201:
              description: Update Redis database with examples
        """
        try:
            jobs.job(["initialize", "init"]) # add job to queue with class name and method (no args)
            piece.loaded = True
            logger.info("Initialize Job")
        except Exception as E:
            logger.critical(E)
        else:
            return "Submitted Initialization Job."

    @app.route("/piece/<int:songid>", methods=['GET'])
    def piece_single(songid : int):
        """ Return a piece as JSON
        ---
        get:
          description: Get piece data from Redis.
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
              description: Return a single piece data as JSON
              content:
                application/json:
                  schema: JSON            
        """
        route = f'/piece/{songid}'
        try:
            out = access.get_pieces()[songid]
        except Exception as E: 
            msg = "Invalid SongID parameter. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        # logger.info(f"GET : {route}")
        
        return jsonify(out)

    @app.route("/piece/", methods=['GET'])
    def piece_all():
        """ Return a list of all available pieces as JSON
        ---
        get:
          description: Get piece data from Redis.
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
              description: Return all piece data as JSON
              content:
                application/json:
                  schema: JSON            
        """
        a0 = rq.args.get('start', 0)
        route = '/piece'
        try: st = int(a0)
        except ValueError: 
            msg = "Invalid start parameter. Please input an integer"
            logger.error(f'{route}:{msg}')
            return msg
        # logger.info(f"GET : {route}")
        out = access.get_pieces()[st:]
        print(out)
        return jsonify(out)

    @app.route("/play/<int:songid>", methods=['GET'])
    def play(songid : int):
        """ Play a piece
        ---
        get:
          description: Play a piece from Redis.
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
              description: Play a piece.
              content:
                application/json:
                  schema: JSON            
        """
        route = f'/piece/{songid}'
        try:
            output = access.play_piece(songid)
        except Exception as E: 
            if songid < access.n_piece():
                msg = "Valid SongID: still processing piece. Please check back later."
            else:
                msg = "Invalid SongID: no such piece available yet. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        # logger.info(f"GET : {route}")
    
        return output
        