import os

from itsdangerous import base64_encode

import redis
from flask import Blueprint, jsonify, render_template, redirect
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

    @app.route("/analyze/value/<int:songid>/", methods=['GET','POST'])
    def value_single(songid : int) -> str:
        """ Return emotional value (eV) information for piece as plot
        ---
        get:
          description: Get eV data and return plot.
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
              description: Return a single piece (eV) plot as HTML
              content:
                application/html:
                  schema: HTML   
        post:
          description: Update eV plot for selected piece.
          parameters:
          - name: songid
            in: path
            description: Index (int) select from for the data list.
            required: true
            example: 0
            schema:
              type: number
          responses:
            201:
              description: Redirect url to GET request for this url          
        """
        route = f'/analyze/value/{songid}/'
        if rq.method == 'POST':
            jobs.job(["appfields", "create_eV_plots", songid, True])
            return redirect(f'{options.proxy}{route}')
        resp = redis_client_raw(7).get(f'{songid}_0')
        if resp is None:
            jobs.job(["appfields", "create_eV_plots", songid]) # add job to queue with class name and method and args.
            msg = "No plot available yet; a job was submitted. Please wait a few moments and try again ... \
              If you have done so, then no such piece exists. Check route /piece for all pieces. \
              Check route /queue for job information."
            logger.error(f'{route}:{msg} - redis client did not find image...')
            return msg
        # logger.info(f"GET : {route}")
        byte = resp.decode("utf-8").replace("\n", "")
        return render_template(
          "img.jinja2",
          template='audio',
          img=byte,
          id=songid,
          proxy=options.proxy
          # img=resp,
        )

    @app.route("/analyze/st/<int:songid>/", methods=['GET','POST'])
    def st_single(songid : int) -> str:
        """ Return s-t coordinate information for piece as plot
        ---
        get:
          description: Get st data and return plot.
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
              description: Return a single piece (st) plot as HTML
              content:
                application/html:
                  schema: HTML   
        post:
          description: Update st plot for selected piece.
          parameters:
          - name: songid
            in: path
            description: Index (int) select from for the data list.
            required: true
            example: 0
            schema:
              type: number
          responses:
            201:
              description: Redirect url to GET request for this url          
        """
        route = f'/analyze/value/{songid}/'
        if rq.method == 'POST':
            jobs.job(["appfields", "create_dst_plots", songid, True])
            return redirect(f'{options.proxy}{route}')
        resp = redis_client_raw(7).get(f'{songid}_1')
        if resp is None:
            jobs.job(["appfields", "create_dst_plots", songid]) # add job to queue with class name and method and args.
            msg = "No plot available yet; a job was submitted. Please wait a few moments and try again ... \
              If you have done so, then no such piece exists. Check route /piece for all pieces. \
              Check route /queue for job information."
            logger.error(f'{route}:{msg} - redis client did not find image...')
            return msg
        # logger.info(f"GET : {route}")
        byte = resp.decode("utf-8").replace("\n", "")
        return render_template(
          "img.jinja2",
          template='audio',
          img=byte,
          id=songid,
          proxy=options.proxy
          # img=resp,
        )

    @app.route("/analyze/PCA/emotion/", methods=['GET','POST'])
    def pca_ev() -> str:
        """ Return emotional value (eV) information for all pieces as a single, PCA plot
        ---
        get:
          description: Get eV data from Redis.
          security:
            - ApiKeyAuth: []
          responses:
            200:
              description: Return a 2D chordspace plot of all pieces (the eV) as HTML
              content:
                application/html:
                  schema: HTML            
        """
        route = '/analyze/PCA/emotion/'
        if rq.method == 'POST':
            jobs.job(["appfields", "create_eV_plot", -1, True]) 
            return redirect(f'{options.proxy}{route}')
        resp = redis_client_raw(7).get('value')
        if resp is None:
            jobs.job(["appfields", "create_eV_plot", -1]) # add job to queue with class name and method and args.
            msg = "No plot available yet; a job was submitted. Please wait a few moments and try again ... \
              If you have done so, then no such piece exists. Check route /piece for all pieces. \
              Check route /queue for job information."
            logger.error(f'{route}:{msg} - redis client did not find image...')
            return msg
        # logger.info(f"GET : {route}")
        byte = resp.decode("utf-8").replace("\n", "")
        return render_template(
          "img2.jinja2",
          template='img',
          img=byte,
          # img=resp,
        )

    @app.route("/analyze/PCA/emotion/<int:songid>/", methods=['GET','POST'])
    def pca_ev_single(songid : int) -> str:
        """ Return emotional value (eV) information for a single piece as a PCA plot using chordspace
        ---
        get:
          description: Get eV data from Redis.
          security:
            - ApiKeyAuth: []
          parameters:
          - name: songid
            description: Index (int) of song to plot.
            in: path
            required: true
            example: 0
            schema:
              type: number
          responses:
            200:
              description: Return a 2D chordspace plot of a single piece eV as HTML
              content:
                application/html:
                  schema: HTML      
        post:
          description: Update eV-PCA plot for selected piece.
          parameters:
          - name: songid
            description: Index (int) of song to plot.
            in: path
            required: true
            example: 0
            schema:
              type: number
          responses:
            201:
              description: Redirect url to GET request for this url        
        """
        route = f'/analyze/PCA/emotion/{songid}/'
        if rq.method == 'POST':
            jobs.job(["appfields", "create_eV_plot", songid, True]) 
            return redirect(f'{options.proxy}{route}')
        resp = redis_client_raw(7).get(f'value_{songid}')
        if resp is None:
            jobs.job(["appfields", "create_eV_plot",songid]) # add job to queue with class name and method and args.
            msg = "No plot available yet; a job was submitted. Please wait a few moments and try again ... \
              If you have done so, then no such piece exists. Check route /piece for all pieces. \
              Check route /queue for job information."
            logger.error(f'{route}:{msg} - redis client did not find image...')
            return msg
        # logger.info(f"GET : {route}")
        byte = resp.decode("utf-8").replace("\n", "")
        return render_template(
          "img2.jinja2",
          template='img',
          img=byte,
          # img=resp,
        )
        