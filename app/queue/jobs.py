# make different types of jobs

from datetime import datetime
import uuid
import json as js

import logging
logger = logging.getLogger('root')

from app.options import options
from app.schema import *
from app.redisclient import redis_client
from hotqueue import HotQueue as qu

class jobs:

    q = qu("queue", host=options.redhost, port=options.redport, db=0)
    rd = redis_client(1)
    max_job_id = 1000000
    last_job_id = -1

    def generate_jid():
        """
        Generate a pseudo-random identifier for a job.
        """
        return str(uuid.uuid4())

    @staticmethod
    def generate_job_key(jid):
        """
        Generate the redis key from the job id to be used when storing, retrieving or updating
        a job in the database.
        """
        return f'job.{jid}'

    @staticmethod
    def job(msg,idmod=None):
        """
        API route for creating a new job to do some analysis. This route accepts a JSON payload
        describing the job to be created.
        (A route in the /api folder will be added for this function)
        Args:
            msg (list) : the input message that calls a specific backend function.
            msg[0] is the class/module, msg[1] the function name, while the rest are arguments.
            idmod (str): any extra specifier for sorting.
        """
        try:

            idn = jobs.last_job_id + 1
            if idn > jobs.max_job_id:
                idn = 0
            
            jid = jobs.generate_jid()

            if idmod is not None: 
                idstring = f'{idmod}:{idn+1}' # mainly for worker-generated subjobs
            else:
                idstring = f'{idn}:0' # for api-generated jobs

            cjob = {
                'id'        : idstring, # internal id to keep track of nth job (important only for timeline-sorted output)
                'uid'       : jid,
                'status'    : "Queued",
                'start'     : "-",
                'end'       : "-",
                'class'    : msg[0],
                'function'  : msg[1],
                'args'      : js.dumps(msg[2:]),
                'output'    : "-"
            }

            jobs.last_job_id = idn

            if len(jobs.q) > jobs.max_job_id - 2:
                logger.warn("overflowing Job Queue; increasing size...")
                jobs.max_job_id += 10

            logger.info("Generated Job.")
            jobs.save_job(jobs.generate_job_key(jid),cjob)
            logger.info("Saved job.")
            jobs.queue_job(jid)
            logger.info("Queued job.")

        except Exception as e:
            logger.error(f"Job Initialization Exception: {e}")
            return True, js.dumps({'status': "Error", 'message': f'Invalid JSON: {e}.'})
        return js.dumps(cjob)

    @staticmethod
    def save_job(job_key, job_dict):
        """Save a job object in the Redis database."""
        logger.info(job_dict)
        jobs.rd.hset(job_key,mapping=job_dict)

    @staticmethod
    def queue_job(jid):
        """Add a job to the redis queue."""
        jobs.q.put(jid)

    @staticmethod
    def update_job_status(jid, status): 
        """Update the status of job with job id `jid` to status `status`."""
        if job := jobs.get_job_by_id(jid):
            job['status'] = status
            jobs.save_job(jobs.generate_job_key(jid), job)
        else:
            raise KeyError("Cannot update status; job does not exist.")

    @staticmethod
    def update_job_time(jid, key): 
        """Update time of job with job id `jid` with key `key`."""
        if job := jobs.get_job_by_id(jid):
            job[key] = str(datetime.now())
            jobs.save_job(jobs.generate_job_key(jid), job)
        else:
            raise KeyError("Cannot update time; job does not exist.")
    
    @staticmethod
    def update_job_output(jid, output): 
        """Update time of job with job id `jid` with output `output`."""
        if job := jobs.get_job_by_id(jid):
            job['output'] = output
            jobs.save_job(jobs.generate_job_key(jid), job)
        else:
            raise KeyError("Cannot update output; job does not exist.")

    @staticmethod
    def get_job_by_id(jid):
        return jobs.rd.hgetall(jobs.generate_job_key(jid))
