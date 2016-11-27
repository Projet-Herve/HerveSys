import sys, os
import json

from functools import wraps
from flask import *

import job
from time import sleep
import schedule,threading

import loads_plugins
import qreaction

setings = json.loads(open("datas/setings.json").read())
argv = sys.argv[1:]

webapp = Flask(__name__)
script_path = os.path.dirname(os.path.realpath(__file__))

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
    
@webapp.route('/index')
@webapp.route('/')
def index():
    return render_template("web/index.html")
    
# loads_plugins.web(webapp,["error","mywash","calandar"])
loads_plugins.web(webapp,["error"])

def myjob():
    job.theme_update(setings)

def fortrue():
	while True:
	    schedule.run_pending()
	    sleep(1)


if "run" in argv:
    myjob()
    schedule.every(setings["theme"]["update_time"]).seconds.do(myjob)
    threading.Thread(target=fortrue).start()
    threading.Thread(target=qreaction.scanner_qr).start()
    
    host = "localhost"
    port = 8080
    
    if "--host" in argv:
        host = argv[argv.index("--host")+1]
    if "-h" in argv:
        host = argv[argv.index("-h")+1]
    if "--port" in argv:
        port = int(argv[argv.index("--port")+1])
    if "-p" in argv:
        port = int(argv[argv.index("-p")+1])
        
    webapp.run(host=host,port=port,debug=True)