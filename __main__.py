import sys, os

from functools import wraps
from flask import *
from flask import session

import job
from time import sleep
import schedule,threading
import hashlib

import qreaction
from myhtml import tag
from datas import load_datas,update_datas
from jms import parse
from notify import *

argv = sys.argv[1:]

webapp = Flask(__name__)
webapp.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
script_path = os.path.dirname(os.path.realpath(__file__))

class herveapp:
	def __init__(self):
		self.settings = json.loads(open("datas/settings.json").read())
		self.users = dict()
		for user in self.settings :
			self.users[user] = {
					"apps" : {},
					"menu" : {"Accueil":"/","Déconnexion":"logout","Apps":"/apps"},
					"widgets" : [],
					#"agenda" : agenda()
				}

myapp = herveapp()

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


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
	datas = load_datas("settings")
	if request.method == 'POST':
		nom = str(request.form.get('nom'))
		code1 = request.form.get('code1')
		code2 = request.form.get('code2')
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
				"code":hashlib.sha224(code1.encode('utf8')).hexdigest()
			}
			session['utilisateur'] = nom
			user = {
				nom:{
					"profile":nouveauutilisateur,
					"installed_apps": [
						"meteo"
				]
				}
			}
			datas.update(user)
			myapp.users.update(user)
			update_datas(datas,"settings")
			message["succes"].append('Bravo '+nom+" vous etes des à present inscrit! Ceci est votre DashBoard")
			updateuserdatas()
		return render_template("web/default/index.html",datas=locals(),myapp = myapp)
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
			if load_datas("settings").get(request.form.get("nom")):
				if load_datas("settings")[request.form.get("nom")]["profile"]["code"] == hashlib.sha224(request.form.get("code").encode('utf8')).hexdigest() :
					session["utilisateur"] = request.form.get("nom")
			if not session.get("utilisateur") :
				message["error"].append("Vous n'avez pas pu etre connecté")
			else :
				message["succes"].append("Vous etes connecté")
		if  len(message["error"])  == 0 :
			return render_template("web/default/index.html",datas=locals(),myapp = myapp)
	return render_template("web/default/connexion.html",datas=locals(),myapp = myapp)

@webapp.route('/widgets',methods=['POST'])
@login_required
def widget():
	user = request.form.get("user")
	toreturn =json.dumps(myapp.users[user]["widgets"])
	return(Response(response=toreturn,status=200,mimetype="application/json"))
	
@webapp.route('/logout')		
def deconnexion():
	message = {}
	if session.get("utilisateur"):
		del(session["utilisateur"])
		message["succes"] =['Vous avez été deconnecté']
	else:
		message["error"] =['Vous n\'étiez pas connecté']
	return render_template("web/default/connexion.html",datas=locals(),myapp = myapp)


def loadsystemdatas():
	for app in myapp.settings["sys"]["installed_apps"]:
		dir = app
		file = app+".py"
		if os.path.isdir("apps/"+dir):
			app_src = open("apps/"+dir+"/"+file)
			src = app_src.read()
			try:
				exec(src)
			except Exception as e:
				print("\nUne erreur est survenu lors de l'éxécution du module "+dir)
				print("----------------------------\n",e,"\n----------------------------\n")
		else :
			print ("L'application '"+dir+"' n'éxiste pas !")

def updateuserdatas():
	for user in myapp.settings:
		for app in myapp.settings[user]["actived_apps"]:
			dir = app
			file = app+".py"
			if os.path.isdir("apps/"+dir):
				manifest = json.loads(open("apps/"+dir+"/manifest.json").read())
				myapp.users[user]["widgets"].extend(manifest["widgets"])
				myapp.users[user]["menu"].update(manifest["urls"]["menu"])
				myapp.users[user]["apps"].update({manifest["displayName"]:manifest})
			else :
				print ("L'application '"+dir+"' n'éxiste pas !")
        
	
def myjob():
	#print("job")
	#send_pushbullet_note("Bonjour","BOJOUR")
	pass

def for_true():
	while 1:
		try :
			schedule.run_pending()
			sleep(2)
		except:
			break

if "run" in argv:
    loadsystemdatas()
    updateuserdatas()
    schedule.every(10).seconds.do(myjob)
    #schedule.every(myapp.settings["theme"]["update_time"]).seconds.do(myjob)
    threading.Thread(target=for_true).start()
    #threading.Thread(target=qreaction.scanner_qr).start()
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