import sys, os
import json

from functools import wraps
from flask import *
from flask import session

import job
from time import sleep
import schedule,threading

import qreaction
from myhtml import tag
from datas import load_datas,update_datas
from jms import parse



argv = sys.argv[1:]

webapp = Flask(__name__)
webapp.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

script_path = os.path.dirname(os.path.realpath(__file__))

class herveapp:
	def __init__(self):
		self.menu = {"Accueil":"/","Déconnexion":"logout","Apps":"/apps"}
		self.widgets = [".humanoid_top_area http://www.frandroid.com"]
		self.settings = json.loads(open("datas/settings.json").read())
		self.apps = {}

		

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

myapp = herveapp()

@webapp.errorhandler(404)
def page_not_found(e):
    return render_template('web/default/error.html',datas=locals(),myapp = myapp)

@webapp.errorhandler(403)
def Forbidden(e):
    return render_template('web/default/error.html',datas=locals(),myapp = myapp)

@webapp.errorhandler(500)
def Internal_Server_Error(e):
    return render_template('web/default/error.html',datas=locals(),myapp = myapp)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("utilisateur"):
            return redirect("/connexion", code=302)
        return f(*args, **kwargs)
    return decorated_function
    
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
	if session.get("utilisateur") :
		return render_template("web/default/index.html",datas=locals(),myapp = myapp)
	else :
		return redirect("/connexion", code=302)
		

@webapp.route('/static/jms/<script>')
def jms_page(script):
	try :
		return Response(response=parse(open('static/jms/'+script,'r').read()),status=200,mimetype="text/javascript")
	except:
		return Response(response="console.log('Fichier jms non trouvé ! (Fichier : " + script +") ; Ou erreur interne du au serveur :/');",status=200,mimetype="text/javascript")

@webapp.route('/apps', methods=['GET'])
@login_required
def apps():
	return render_template("web/default/apps.html",datas=locals(),myapp=myapp)

@webapp.route('/inscriptions', methods=['GET','POST'])
def inscriptions():
	datas = load_datas("users.json")

	if request.method == 'POST':
		nom = str(request.form.get('nom'))
		code1 = int(request.form.get('code1'))
		code2 = int(request.form.get('code2'))
		message = {"error":[],"succes":[]}

		if not nom :
			message["error"].append('Veillez choisir un nom d\'utilistaur')

		if not code1 :
			message["error"].append('Veillez choisir un code de securite')

		if not code2 :
			message["error"].append('Veillez retapper votre code de securite')

		if code1 != code2 :
			message["error"].append('Veillez entrer deux fois le meme code')		
		
		if not message['error']:
			nouveauutilisateur = {
				"id":len(datas),
				"nom":nom,
				"code":code1*22*10/11
			}
			session['utilisateur'] = nom
			user = {nom:nouveauutilisateur}
			datas.update(user)
			update_datas(datas,"users.json")
			message["succes"].append('Bravo '+nom+" vous etes des a present inscrit! Vous pouvez dessormais accerder au <a href='/'>dashboard</a>.")
		return render_template("web/default/inscriptions.html",datas=locals(),myapp = myapp,messages=message)
	else :
		return render_template("web/default/inscriptions.html",datas=locals(),myapp = myapp)
		
@webapp.route('/connexion', methods=['GET','POST'])
def connexion():
	if request.method == "POST":
		message = {"error":[],"succes":[]}
		if not request.form.get("nom") :
			message["error"].append("Vous devez entrer votre nom d'utilisateur")
		if not request.form.get("code") :
			message["error"].append("Vous devez entrer votre code")
		if request.form.get("code") and request.form.get("nom") :
			if load_datas("users.json").get(request.form.get("nom")):
				if load_datas("users.json")[request.form.get("nom")]["code"] == int(request.form.get("code"))*22*10/11 :
					session["utilisateur"] = request.form.get("nom")
			if not session.get("utilisateur") :
				message["error"].append("Vous n'avez pas pu etre connecté")
			else :
				message["succes"].append("Vous etes connecté")
		if  len(message["error"])  == 0 :
			return render_template("web/default/index.html",datas=locals(),myapp = myapp)
	return render_template("web/default/connexion.html",datas=locals(),myapp = myapp)
		
@webapp.route('/logout')		
def deconnexion():
	message = {}
	if session.get("utilisateur"):
		del(session["utilisateur"])
		message["succes"] =['Vous avec été deconnecté']
	else:
		message["error"] =['Vous n\'etiez pas connecté']
	return render_template("web/default/connexion.html",datas=locals(),myapp = myapp)

	


for app in myapp.settings["installed_apps"]:
    dir = app
    file = app+".py"
    if os.path.isdir("apps/"+dir):
        app_src = open("apps/"+dir+"/"+file)
        src = app_src.read()
        exec(src)
        manifest = json.loads(open("apps/"+dir+"/manifest.json").read())
        myapp.widgets.extend(manifest["widgets"])
        myapp.menu.update(manifest["urls"]["menu"])
        myapp.apps.update({manifest["displayName"]:manifest})
    else :
        raise appnotexist("L'application '"+dir+"' n'existe pas !")
	
def myjob():
	print("job")

def for_true():
	while True:
	    schedule.run_pending()
	    sleep(1)


if "run" in argv:
    #myjob()
    #schedule.every(myapp.settings["theme"]["update_time"]).seconds.do(myjob)
    #threading.Thread(target=for_true).start()
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