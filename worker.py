import sys
import app.options
# set Redis IP
print(f"Args: {sys.argv}")
ipa = sys.argv[1]
app.options.options.sethost(ipa)
# make and start a worker
from app.queue.worker import worker as wk
wk().execute_job()