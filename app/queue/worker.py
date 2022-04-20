# take whatever argument enters and run that
import json as js
import os
from app.queue.jobs import jobs
import logging
logger = logging.getLogger('root')

# automatic import

visible_dir = ['app/quarry/']
denylist = ['__pyc','__init','README']
methods = []
for folder in visible_dir:
    for file in os.listdir(folder):
        if all(item not in file for item in denylist):
            page = file[:len(file)-3]
            modname = folder.replace('/','.')
            exec(f'from {modname}{page} import {page}')


class worker:

    @jobs.q.worker
    def execute_job(self,jid):
        jobs.update_job_status(jid, 'Started')
        job = jobs.get_job_by_id(jid)
        jobs.update_job_time(jid,'start')
        #---
        function = getattr(globals()[job['class']],job['function'])
        args = js.loads(job['args'])
        logger.info(f"Running function {job['function']} from class/module {job['class']} with args: [{','.join(args)}]")
        output = function(*args) if len(args) > 0 else function()
        if output is None:
            output = 'None'
        jobs.update_job_output(jid,output)
        #---
        jobs.update_job_time(jid,'end')
        jobs.update_job_status(jid, 'Completed')
