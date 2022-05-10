from flask import jsonify, redirect, render_template
from flask import current_app as app
from flask import request as rq
import requests as rqs
import json as js
import base64

from flask_apispec import MethodResource

import logging
logger = logging.getLogger('root')

from app.options import options
from app.schema import *
from app.redisclient import redis_client,redis_client_raw

import pickle

from app.queue.jobs import jobs
from app.shaft import access
# IMPORTANT: make sure to name the class you use the same as the filename!
# IMPORTANT: any non-route methods should not be in the class!
class piece(MethodResource):

    loaded = False     

    rd3 = redis_client(3) # for generic data
    rd4 = redis_client_raw(4) # for musicpy objects 

    @app.route("/init", methods=['POST'])
    def init() -> str:
        """Set up all example pieces in repository
        ---
        post:
          description: Create examples.
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

    ################## CREATE/READ/UPDATE/DELETE methods ###########################
    # GET Single
    @app.route("/piece/<int:songid>/", methods=['GET'])
    def piece_single(songid : int) -> str:
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
            schema:
              type: number
          responses:
            200:
              description: Return a single piece data as JSON
              content:
                application/json:
                  schema: JSON            
        """
        route = f'/piece/{songid}/'
        try:
            out = access.get_pieces()[songid]
        except Exception as E: 
            msg = "Invalid SongID parameter. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        # logger.info(f"GET : {route}")
        
        return jsonify(out)

    # GET All
    @app.route("/piece/", methods=['GET'])
    def piece_all() -> str:
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
            schema:
              type: number
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

    #GET bpm
    @app.route("/piece/<int:songid>/bpm/", methods=['GET'])
    def piece_bpm(songid : int) -> str:
        """Return the beats per minute (BPM) of a piece as JSON
        ---
        get:
          description: Get BPM data for a piece from Redis.
          security:
            - ApiKeyAuth: []
          parameters:
          - name: songid
            in: path
            description: Index (int) select from for the data list.
            required: true
            example: 0
            schema:
              type: number
          responses:
            200:
              description: Return BPM data for a piece as JSON
              content:
                application/json:
                  schema: JSON
        """
        route = f'/piece/{songid}/bpm/'
        try:
            out = access.get_pieces()[songid]["bpm"]
        except Exception as E:
            msg = "Invalid SongID parameter. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        return jsonify(out)

    # CREATE
    # create a song from a chord progression
    @app.route("/piece/CREATE", methods=['POST'])
    def piece_create():
        """
        Replaces a song-data object in the songbank with user inputted namesake.
        --- 
        post:
          description: Update a song in the songbank.
          requestBody:
            description: Chord progression JSON input
            required: true
            content:
              application/json:
                example: {"name":"Progression0","bpm":174,"chord":[{"chd":"Cm7","time":0.5,"arp":0.125,"start":0,"inst":"Acoustic Grand Piano"},{"chd":"Dsus","time":0.5,"arp":0.125,"start":0.5,"inst":"Acoustic Grand Piano"},{"chd":"Caug7","time":0.5,"arp":0.125,"start":1,"inst":"Acoustic Grand Piano"},{"chd":"Dadd2","time":0.5,"arp":0.125,"start":1.5,"inst":"Acoustic Grand Piano"},{"chd":"Cm7","time":0.5,"arp":0.125,"start":2,"inst":"Acoustic Grand Piano"},{"chd":"Dsus","time":0.5,"arp":0.125,"start":2.5,"inst":"Acoustic Grand Piano"},{"chd":"Caug7","time":0.5,"arp":0.125,"start":3,"inst":"Acoustic Grand Piano"},{"chd":"D,G,A,A# / Dadd2","time":0.5,"arp":0.25,"start":3.5,"inst":"Acoustic Grand Piano"}]}
          responses:
            201:
              description: Return a confirmation message stating that the update was a success.         
        """
        route = '/piece/CREATE'
        try:
            jsm = rq.json
            
            encoded = base64.b64encode(pickle.dumps(jsm['chord']))
            cs = encoded.decode('ascii')
            logger.info(cs)

            jobs.job(["initialize", "init_chd", cs, jsm['bpm'], jsm['name']])
        except Exception as E:
            msg = f'Invalid JSON or other error. Exception: {E}.'
            logger.error(f'{route}:{msg}')
            return msg
        return 'Successfully Added.'

    # UPDATE
    # update a song by replacing it with a user-uploaded version
    @app.route("/piece/<int:songid>/UPDATE", methods=['POST'])
    def piece_update(songid : int):
        """
        Replaces a song-data object in the songbank with user input.
        --- 
        post:
          description: Update a song in the songbank.
          parameters:
          - name: songid
            in: path
            description: Index of song to update in songbank.
            required: true
            example: 1
            schema:
              type: number
          requestBody:
            description: Chord progression JSON input
            required: true
            content:
              application/json:
                example: {"name":"Progression0","bpm":174,"chord":[{"chd":"Cm7","time":0.5,"arp":0.125,"start":0,"inst":"Acoustic Grand Piano"},{"chd":"Dsus","time":0.5,"arp":0.125,"start":0.5,"inst":"Acoustic Grand Piano"},{"chd":"Caug7","time":0.5,"arp":0.125,"start":1,"inst":"Acoustic Grand Piano"},{"chd":"Dadd2","time":0.5,"arp":0.125,"start":1.5,"inst":"Acoustic Grand Piano"},{"chd":"Cm7","time":0.5,"arp":0.125,"start":2,"inst":"Acoustic Grand Piano"},{"chd":"Dsus","time":0.5,"arp":0.125,"start":2.5,"inst":"Acoustic Grand Piano"},{"chd":"Caug7","time":0.5,"arp":0.125,"start":3,"inst":"Acoustic Grand Piano"},{"chd":"D,G,A,A# / Dadd2","time":0.5,"arp":0.25,"start":3.5,"inst":"Acoustic Grand Piano"}]}
          responses:
            201:
              description: Return a confirmation message stating that the update was a success.         
        """
        route = f'/piece/{songid}/UPDATE'
        try:
            jsm = rq.json

            encoded = base64.b64encode(pickle.dumps(jsm['chord']))
            cs = encoded.decode('ascii')
            logger.info(cs)

            jobs.job(["initialize", "init_chd", cs, jsm['bpm'], jsm['name'], songid])
        except Exception as E:
            msg = 'Song not in database.'
            logger.error(f'{route}:{msg}. Exception: {E}.')
            return msg
        return 'Successfully updated.'
      
    # DELETE
    # delete a specific song from the songbank
    # unfortunately an O(n) operation, since otherwise we would have 'empty' key problems
    # Would be better to have a list-style structure in Redis, but unfortunately that is not possible 
    # (note not referring to a list object, but rather a list access over a dict key-based access for Redis)
    @app.route("/piece/<int:songid>/DELETE", methods=['POST'])
    def piece_delete(songid : int):
        """
        Takes a song id and deletes that song from the songbank.
        --- 
        post:
          description: Delete a song from the songbank.
          parameters:
          - name: songid
            in: path
            description: Index of song to delete from songbank.
            required: true
            example: 0
            schema:
              type: number
          responses:
            201:
              description: Return a deletion confirmation message.          
        """
        # n_keys = len(piece.rd3.keys())
        # for i in range(n_keys):
        #     to_delete = piece.rd3.get(str(i))
        #     delName = to_delete['name']
        #     if( delName.lower() == name.lower()):
        route = f'/piece/{songid}/DELETE'
        try:
            for key in range(songid,access.n_piece()-1):
                # all later keys - push up - cannot be parallelized at the moment.
                access.hrename(3,key+1,key)
                access.rename_raw(4,key+1,key)
        except Exception as E:
            msg = 'Song not in database.'
            logger.error(f'{route}:{msg}. Exception: {E}.')
            return msg
        return 'Successfully deleted.'

    ############## songbank route #######################   
    # basically the gui for the above CUD:
    @app.route('/songbank', methods=['GET','POST'])
    def songbank() -> str:
        """
        Songbank GUI. Generates POST requests as necessary.
        ---
        get:
          description: Get songbank GUI.
          security:
            - ApiKeyAuth: []
          responses:
            200:
              description: Return songbank GUI as HTML.
              content:
                application/json:
                  schema: HTML      
        post:
          description: Call necessary routes with given input.
          responses:
            201:
              description: Redirect url to GET request for this url.
        """
        if rq.method != 'POST':
            return render_template(
              "io.jinja2",
              proxy=options.proxy
            )
        route="/songbank"
        try:
          dat = rq.form.to_dict()
          op = dat['operation']
          logger.info(f'operation on {route} : {op}')

          if op in ['UPDATE', 'DELETE']:
            idr = int(dat['id'])

          if op in ['CREATE', 'UPDATE']:
            nm = dat['name']
            bpm = float(dat['bpm'])
            chd = js.loads(dat['chord'])
            data = {'name':nm,'bpm':bpm,'chord':chd}

          base = rq.url_root

          if op == 'CREATE':
            rqs.post(f'{base}/piece/{op}', json=data)
          elif op == 'UPDATE':
            rqs.post(f'{base}/piece/{idr}/{op}', json=data)
          elif op == 'DELETE':
            rqs.post(f'{base}/piece/{idr}/{op}')
          else:
            raise(op)
        except Exception as E: 
          logger.error(f'{route} had exception: {E}')
          print(E)
          return f"Invalid JSON, possibly. Had exception: {E}"
        return redirect("")

    ############## play route #######################

    @app.route("/play/<int:songid>/", methods=['GET'])
    def play(songid : int) -> str:
        """ Play a piece.
        ---
        get:
          description: Play a piece from Redis.
          security:
            - ApiKeyAuth: []
          parameters:
          - name: songid
            in: path
            description: Index of song to play from songbank.
            required: true
            example: 0
            schema:
              type: number
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
        
