@webapp.route('/mywash', methods=['GET'])
@login_required
@need_app_active
def index_mywash():
	mywashdatas = json.loads(open("datas/apps/mywash/mywash.json","r").read())
	users = load_datas("settings")
	return render_template("apps/mywash/index.html",datas=mywashdatas,users=users,myapp=myapp)

