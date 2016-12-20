import json
from flask import *
from __main__ import login_required
 

#webapp = datas["webapp"]
@webapp.route('/mywash', methods=['GET'])
@login_required
def index_mywash():
	mywashdatas = json.loads(open("datas/apps/mywash/mywash.json","r").read())
	users = load_datas("settings")
	return render_template("web/apps/mywash/index.html",datas=mywashdatas,users=users,myapp=myapp)

