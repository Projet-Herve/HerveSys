import json
from flask import *
from __main__ import login_required

@webapp.route('/cozy')
@login_required
def cozy_index():
    # Vote code pour cozy
    return render_template("cozy/templates/index.html",datas=locals())
