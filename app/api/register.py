from flask import Blueprint, jsonify, render_template, redirect
from flask import current_app as app
from flask import request as rq

from flask_apispec import use_kwargs, marshal_with
from flask_apispec.views import MethodResource
from app.schema import * #schema

import logging
logger = logging.getLogger('root')

import requests as rqs
import json as js
import numpy as np
import markdownify as md

from app.options import options

# Not pytesting the following functions as 1) testing the requests is unecessary, 2) this is not core functionality and is not required by the specifications,
# 3) this is an API test in and of itself, and part of other tests, 4) developer exhaustion...

# this is an api-side request since it really has nothing to do with the application, and is fast enough of a site scraper. 
# (one could make an equivalent argument that it should be worker-side if completely full-fleshed responses are required --- like all the images..)

def capture(url, type=0, appcontext=None, htm=False) -> object:
  """Parses JSON/HTML from an endpoint.
  Args:
      url (str): A string containing the endpoint URL.
      type (int): GET or POST endpoint?
      appcontext (object): None if not testing.
      htm (bool): flag to set True if endpoint is HTML.
  Returns:
      dict: the Python dictionary version of the input url JSON.
      OR 
      str:  a HTML string version of the input url.
  """
  data = lambda x,appcontext: x.data if appcontext is not None else x.content
  decode = lambda x,appcontext: js.loads(data(x,appcontext).decode('utf8').replace("'", '"'))

  rqx = rqs if appcontext is None else appcontext
  cap = rqx.get(url) if type==0 else rqx.post(url)
  out = data(cap,appcontext).decode('utf8').replace("'", '"') if htm else decode(cap,appcontext)
  logger.info(out)
  return out

def callresponse(i,k,path,values,io,rest,denylist,appcontext) -> list:
  """The example call and response section from the generateAPI function.
  Args:
      i (int): io array index (current function id).
      k (int): endpoint type index.
      path (str): endpoint path.
      values (dict): a dictionary describing parameters.
      io (np.ndarray): an array containing all possible api information.
      rest (str): endpoint type.
      denylist (list): endpoints not considered.
      appcontext (object): None if not testing.
  Returns:
      int: success of API call (will be zero for success and expected fails).
      str: the resulting response.
  """
  state = 0
  if values is not None:
    segmented = np.array(path.replace("{","}").split("}"))
    odd = (np.array(list(range(len(segmented)))) % 2 == 1)
    # logger.info(segmented[odd])
    exval = [values[c] for c in segmented[odd]]
    # logger.info(exval)
    call = "".join([str(exval[int(j/2)]) if odd[j] else str(segmented[j]) for j in range(len(segmented))])
    # logger.info(call)
  else:
    call = path
  url = f"{options.getURL()}{call}"
  io[i,4] = f"`curl -X {rest} {url} -H \"accept: application/json\"`"
  logger.info(f"CALL:{url}")

  if call not in denylist:
    try:
      rawstringjs = js.dumps(capture(url,k,appcontext), indent=4, sort_keys=True)
    except Exception as e:
      try: # assume HTML instead
        rawstringjs = md.markdownify(capture(url,k,appcontext,htm=True), heading_style="ATX")
      except Exception as e:
        msg = "API CALL FAILED"
        logger.warn(f"{msg} : {url} | {e}")
        rawstringjs = msg
        state = 1
    logger.info(rawstringjs)
    segmented = rawstringjs.split("\n")
    lox = len(segmented)
    if lox > 30:
      stringjsA = segmented[:15]
      stringjsA.extend(["...."])
      stringjsA.extend(segmented[lox-15:lox])
      rawstringjs = "\n".join(stringjsA)
    exresp = f"\n{rawstringjs}"
  else:
    exresp = None
    rawstringjs = "Not Shown."
  io[i,5] = exresp
  logger.info(f"OUT:{exresp}")
  return state,rawstringjs

# really should split this function...

def generateAPI(api,test=False,badvalues=False,appcontext=None) -> np.ndarray:
  """Structure API information (currenly assumes single endpoint: either GET or POST, not both).
  Arguments: 
    api (dict): The API dictionary parsed by FlaskApiSpec.
    test (bool): Save test outputs?
    badvalues (bool): Use bad values for testing?
    appcontext (object): None if not testing?
  Returns:
    array: a NumPy array structure containing endpoints, descriptions, parameter names&descriptions, response descriptions, example input calls, example outputs. 
      If test is true, then only the outputs are returned.
  """
  REST = ["get","post"]
  REST2 = ["GET","POST"]
  p = 'parameters'
  paths = api['paths'].keys()
  denylist = ['/','/pdf','/api/save','/api/doc']
  badval = "3"
  # make i/o array

  io = np.zeros(shape=(len(paths),6),dtype=object) # endpoint,description, parameter names&descriptions, response descriptions, example input call, example output

  if test:
    exa = np.zeros(shape=(len(paths)),dtype=tuple(list,bool,object)) #  endpoint, status, example output

  # loop over API

  for i, pinfo in enumerate(zip(paths,api['paths'].values())):
    # logger.info(info['options'])
    path, info = pinfo
    io [i,0] = path

    for k,key in enumerate(REST):
      if key in info.keys():
        endpoint = info[key]
        io [i,1] = endpoint['description']
        logger.info(f"DESC:{endpoint['description']}")

        if p in endpoint.keys():
          params = endpoint['parameters']
          values = dict([(pq['name'],pq['example']) for pq in params])
          namedesc = [f"`{pq['name']}`\t:\t{pq['description']}\tAn example would be : `{pq['example']}`" for pq in params]
          io[i,2] = namedesc
          # logger.info(values)
          logger.info(f"PARAM:{namedesc}")
        else:
          values = None
          io [i,2] = ["N/A"]

        resp = endpoint['responses']
        respdesc = [f"A `{ret}` response will : {resp[ret]['description']}" for ret in resp.keys()]
        io[i,3] = respdesc
        logger.info(f"RESP:{respdesc}")

        if not badvalues:
          state,rawstringjs = callresponse(i,k,path,values,io,REST2[k],denylist,appcontext)
        else: # testing API
          state = 1
          if values is not None:
            valuelen = len(values)
            for r in range(valuelen):
              val2 = values[:r]
              val2.extend([badval])
              val2.extend(values[r+1:])
            state2,rawstringjs = callresponse(i,k,path,val2,io,REST2[k],denylist,appcontext)
            state *= state2
          else:
            rawstringjs = "No testable parameters"

        break # remember, single endpoints!

    if test:
      if badvalues: 
        state = 1-state
      try: exa[i] = (path,state,js.loads(rawstringjs))
      except Exception: exa[i] = (path,state,rawstringjs)

  if test:
    return exa
  return io


def formatAPI(io) -> str:
  """Structure API information.
  Args: 
    io (array): a NumPy array structure containing descriptions, parameter names&descriptions, response descriptions, example input calls, example outputs.
  Returns:
    string: a formatted Markdown output
  """
  # io = np.zeros(shape=(len(paths),6),dtype=object) # path,description, parameter names&descriptions, response descriptions, example input call, example output
  out = []
  for i in range(len(io)):
    f = io[i,:]
    path = f"### ENDPOINT: `{f[0]}`"
    desc = f" - Description: {f[1]}"
    param = " - Parameters: \n   -  {}".format("\n   -  ".join(f[2]))
    resp = " - Responses: \n   -  {}".format("\n   -  ".join(f[3]))
    if f[5] is not None:
      opt = " yields: "
      eoc = "```"+"  \n ".join(f[5].split("\n"))+"\n```"
    else:
      opt = ''
      eoc = ''
    eic = f"\n - Example: {f[4]}{opt}"
    st = "\n".join([path,desc,param,resp,eic,eoc])
    out.append(st)
  return "## REST API:\n" + "\n\n".join(out)


class register(MethodResource):

    @app.route("/api/save", methods=['GET'])
    def register() -> str:
        """Application API (generate API examples). UNSUPPORTED, so use at your own risk.
        ---
        get:
          description: Get API as rendered string
          security:
            - ApiKeyAuth: []
          responses:
            200:
              description: Return rendered API as string
              content:
                application/json:
                  schema: SSchema
        """
        route="/api/save"
        try:
            # get api
            url = f"{options.getURL()}/api/api.json"
            api = capture(url)
            io = generateAPI(api)
            markdown = formatAPI(io)
            # with open(options.mdfile,'r') as file:
            #   file.write(markdown)
        except Exception as e: 
            msg = f"Exception: {e}"
            logger.error(f'{route}:{msg}')
            return msg
        else:
            msg = "Generated Examples."
            logger.info(f'{route}:{msg}')
        return markdown
      
    @app.route("/flask-apispec/static/<string:item>", methods=['GET'])
    def apis(item) -> str:
        """A redirect for missing SwaggerUIBundle
        ---
        get:
          description: Get SwaggerUIBundle item as necessary
          security:
            - ApiKeyAuth: []
          responses:
            200:
              description: Return SwaggerUIBundle url redirect
              content:
                application/json:
                  schema: HTML
        """
        route="/static/swagger-ui/"
        return redirect(f'{options.proxy}{route}{item}')

    @app.route("/swagger-ui-bundle.js", methods=['GET'])
    def apistwo() -> str:
        """Another redirect for missing SwaggerUIBundle
        ---
        get:
          description: Get SwaggerUIBundle item as necessary
          security:
            - ApiKeyAuth: []
          responses:
            200:
              description: Return SwaggerUIBundle url redirect
              content:
                application/json:
                  schema: HTML
        """
        route="/static/swagger-ui/swagger-ui-bundle.js"
        return redirect(f'{options.proxy}{route}')
