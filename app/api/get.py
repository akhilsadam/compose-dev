from flask import jsonify
from flask import current_app as app
from flask import request as rq
import json as js
from flask_apispec import MethodResource

import logging
logger = logging.getLogger('root')

from app.schema import *
from app.redisclient import redis_client

from app.shaft import access
# IMPORTANT: make sure to name the class you use the same as the filename!
# IMPORTANT: any non-route methods should not be in the class!
class get(MethodResource):

    ################################ Individual ########################################

    #GET BPM
    @app.route("/piece/bpm/<int:songid>/", methods=['GET'])
    def piece_bpm_single(songid : int) -> str:
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
        route = f'/piece/bpm/{songid}/'
        try:
            out = access.get_pieces()[songid]["bpm"]
        except Exception as E:
            msg = "Invalid SongID parameter. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        return jsonify(out)

    #GET chords
    @app.route("/piece/chords/<int:songid>/", methods=['GET'])
    def piece_chord_single(songid : int) -> str:
        """Return the chords of a piece as JSON
        ---
        get:
          description: Get chord data for a piece from Redis.
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
              description: Return chord data for a piece as a JSON list
              content:
                application/json:
                  schema: JSON
        """
        route = f'/piece/chords/{songid}/'
        try:
            out = js.loads(redis_client(5).hget(songid,'chd'))
        except Exception as E:
            msg = "Either an invalid SongID parameter, or this song is being initialized now. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        return jsonify(out)

    @app.route("/piece/n_chords/<int:songid>/", methods=['GET'])
    def piece_nchord_single(songid : int) -> str:
        """Return the number of chords of a piece as JSON
        ---
        get:
          description: Get number of chords for a piece from Redis.
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
              description: Return number of chords for a piece as a int
              content:
                application/json:
                  schema: JSON
        """
        route = f'/piece/n_chords/{songid}/'
        try:
            out = len(js.loads(redis_client(5).hget(songid,'chd')))
        except Exception as E:
            msg = "Either an invalid SongID parameter, or this song is being initialized now. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        return jsonify(out)

    @app.route("/piece/notes/<int:songid>/", methods=['GET'])
    def piece_notes_single(songid : int) -> str:
        """Return the notes of a piece as JSON
        ---
        get:
          description: Get notes for a piece from Redis.
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
              description: Return notes for a piece as a JSON list
              content:
                application/json:
                  schema: JSON
        """
        route = f'/piece/notes/{songid}/'
        try:
            out = js.loads(redis_client(5).hget(songid,'note'))
        except Exception as E:
            msg = "Either an invalid SongID parameter, or this song is being initialized now. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        return jsonify(out)

    @app.route("/piece/n_notes/<int:songid>/", methods=['GET'])
    def piece_nnotes_single(songid : int) -> str:
        """Return the number of notes of a piece as JSON
        ---
        get:
          description: Get number of notes for a piece from Redis.
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
              description: Return number of notes for a piece as a int
              content:
                application/json:
                  schema: JSON
        """
        route = f'/piece/n_notes/{songid}/'
        try:
            out = len(js.loads(redis_client(5).hget(songid,'note')))
        except Exception as E:
            msg = "Either an invalid SongID parameter, or this song is being initialized now. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        return jsonify(out)

    @app.route("/piece/intervals/<int:songid>/", methods=['GET'])
    def piece_intervals_single(songid : int) -> str:
        """Return the time intervals from the start of the previous note to the start of the current note in bar-units of a piece as JSON
        ---
        get:
          description: Get intervals for a piece from Redis.
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
              description: Return intervals for a piece as a JSON list
              content:
                application/json:
                  schema: JSON
        """
        route = f'/piece/intervals/{songid}/'
        try:
            out = js.loads(redis_client(5).hget(songid,'interval'))
        except Exception as E:
            msg = "Either an invalid SongID parameter, or this song is being initialized now. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        return jsonify(out)

    ############# all pieces at once #######################

    #GET BPM
    @app.route("/piece/bpm/", methods=['GET'])
    def piece_bpm() -> str:
        """Return the beats per minute (BPM) of all pieces as JSON
        ---
        get:
          description: Get BPM data for all pieces from Redis.
          security:
            - ApiKeyAuth: []
          parameters:
          - name: start
            in: query
            description: Index (int) to start iterating from in the data list.
            required: false
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
        route = f'/piece/bpm/'
        try:
            st = int(rq.args.get('start', 0))
            out = access.get_pieces()
            out = [js.loads(o["bpm"]) for o in out[st:]]
        except Exception as E:
            msg = "Invalid start parameter. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        return jsonify(out)

    #GET chords
    @app.route("/piece/chords/", methods=['GET'])
    def piece_chord() -> str:
        """Return the chords of all pieces as JSON
        ---
        get:
          description: Get chord data for all pieces from Redis.
          security:
            - ApiKeyAuth: []
          parameters:
          - name: start
            in: query
            description: Index (int) to start iterating from in the data list.
            required: false
            example: 0
            schema:
              type: number
          responses:
            200:
              description: Return chord data for all pieces as a JSON list
              content:
                application/json:
                  schema: JSON
        """
        route = f'/piece/chords/'
        try:
            st = int(rq.args.get('start', 0))
            rd5 = redis_client(5)
            out = [js.loads(rd5.hget(key,'chd')) for key in sorted(rd5.keys())[st:]]
        except Exception as E:
            msg = "Invalid start parameter. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        return jsonify(out)

    #GET nchords
    @app.route("/piece/n_chords/", methods=['GET'])
    def piece_nchord() -> str:
        """Return the number of chords of all pieces as JSON
        ---
        get:
          description: Get the number of chords for all pieces from Redis.
          security:
            - ApiKeyAuth: []
          parameters:
          - name: start
            in: query
            description: Index (int) to start iterating from in the data list.
            required: false
            example: 0
            schema:
              type: number
          responses:
            200:
              description: Return the number of chords for all pieces as a JSON list
              content:
                application/json:
                  schema: JSON
        """
        route = f'/piece/n_chords/'
        try:
            st = int(rq.args.get('start', 0))
            rd5 = redis_client(5)
            out = [len(js.loads(rd5.hget(key,'chd'))) for key in sorted(rd5.keys())[st:]]
        except Exception as E:
            msg = "Invalid start parameter. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        return jsonify(out)

    @app.route("/piece/notes/", methods=['GET'])
    def piece_notes() -> str:
        """Return the notes for all pieces as JSON
        ---
        get:
          description: Get the notes for all pieces from Redis.
          security:
            - ApiKeyAuth: []
          parameters:
          - name: start
            in: query
            description: Index (int) to start iterating from in the data list.
            required: false
            example: 0
            schema:
              type: number
          responses:
            200:
              description: Return the notes for all pieces as a JSON list
              content:
                application/json:
                  schema: JSON
        """
        route = f'/piece/notes/'
        try:
            st = int(rq.args.get('start', 0))
            rd5 = redis_client(5)
            out = [js.loads(rd5.hget(key,'note')) for key in sorted(rd5.keys())[st:]]
        except Exception as E:
            msg = "Invalid start parameter. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        return jsonify(out)

    @app.route("/piece/n_notes/", methods=['GET'])
    def piece_nnotes() -> str:
        """Return the number of notes for all pieces as JSON
        ---
        get:
          description: Get the number of notes for all pieces from Redis.
          security:
            - ApiKeyAuth: []
          parameters:
          - name: start
            in: query
            description: Index (int) to start iterating from in the data list.
            required: false
            example: 0
            schema:
              type: number
          responses:
            200:
              description: Return the number of notes for all pieces as a JSON list
              content:
                application/json:
                  schema: JSON
        """
        route = f'/piece/n_notes/'
        try:
            st = int(rq.args.get('start', 0))
            rd5 = redis_client(5)
            out = [len(js.loads(rd5.hget(key,'note'))) for key in sorted(rd5.keys())[st:]]
        except Exception as E:
            msg = "Invalid start parameter. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        return jsonify(out)

    @app.route("/piece/intervals/", methods=['GET'])
    def piece_intervals() -> str:
        """Return the time intervals from the start of the previous note to the start of the current note in bar-units for all pieces as JSON
        ---
        get:
          description: Get intervals for a piece from Redis.
          security:
            - ApiKeyAuth: []
          parameters:
          - name: start
            in: query
            description: Index (int) to start iterating from in the data list.
            required: false
            example: 0
            schema:
              type: number
          responses:
            200:
              description: Return intervals for a piece as a JSON list
              content:
                application/json:
                  schema: JSON
        """
        route = f'/piece/intervals/'
        try:
            st = int(rq.args.get('start', 0))
            rd5 = redis_client(5)
            out = [js.loads(rd5.hget(key,'interval')) for key in sorted(rd5.keys())[st:]]
        except Exception as E:
            msg = "Invalid start parameter. Please input an integer in range."
            logger.error(f'{route}:{msg} had exception {E}')
            return msg
        return jsonify(out)

