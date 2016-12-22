import sys, os

from functools import wraps
from flask import *


from time import sleep
import schedule,threading
import hashlib

#import qreaction
from myhtml import tag
from datas import load_datas,update_datas
from jms import parse
from notify import *
import chatbot
argv = sys.argv[1:]

webapp = Flask(__name__)
webapp.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
script_path = os.path.dirname(os.path.realpath(__file__))

class herveapp:
	def __init__(self):
		self.forever_ = []
		self.settings = json.loads(open("datas/settings.json").read())
		self.users = dict()
		for user in self.settings :
			self.users[user] = {
					"apps" : {},
					"menu" : {"Accueil":"/","Déconnexion":"logout","Apps":"/apps","Widgets":"/widgets"},
					"widgets" : list(map(lambda x: x.replace("/","%2F"),self.settings[user]["widgets"])),
					"urls":[]
					#"agenda" : agenda()
				}
				
	def forever(self,function):
		def decorator(function):
			try:
				self.forever_.append(function)
				return True
			except Exception as e:
				print("[erreur] "+e)
				return False
		return decorator(function)
		
	def start(self):
		def __forever():
			while True :
				for function in self.forever_ :
					function()
		def forschedule():
			while True:
				schedule.run_pending()
				sleep(1)
		
		threading.Thread(target=__forever).start()
		threading.Thread(target=forschedule).start()
		#threading.Thread(target=qreaction.scanner_qr).start()
	
myapp = herveapp()

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

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
    
def need_app_active(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		requesturl = "/"+"/".join(request.url.split("/")[3:])
		if not requesturl in myapp.users[session["utilisateur"]]["urls"] :
			return redirect("/",code=302)
		return f(*args, **kwargs)
	return decorated

	
@webapp.errorhandler(404)
def page_not_found(e):
    return render_template('default/error.html',datas=locals(),myapp=myapp)

@webapp.errorhandler(403)
def Forbidden(e):
    return render_template('default/error.html',datas=locals(),myapp = myapp)

@webapp.errorhandler(500)
def Internal_Server_Error(e):
    return render_template('default/error.html',datas=locals(),myapp = myapp)


    
@webapp.route('/index')
@webapp.route('/')
def index():
	if session.get("utilisateur") :
		return render_template("default/index.html",datas=locals(),myapp = myapp)
	else :
		return redirect("/connexion", code=302)
		

@webapp.route('/static/default/jms/<script>')
def jms_page(script):
	try :
		return Response(response=parse(open('static/default/jms/'+script,'r').read()),status=200,mimetype="text/javascript")
	except:
		return Response(response="console.log('Fichier jms non trouvé ! (Fichier : " + script +") ; Ou erreur interne du au serveur :/');",status=200,mimetype="text/javascript")

@webapp.route('/apps', methods=['GET'])
@login_required
def apps():
	return render_template("default/apps.html",datas=locals(),myapp=myapp)

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
					"actived_apps": [
				]
				}
			}
			datas.update(user)
			myapp.users.update(user)
			update_datas(datas,"settings")
			message["succes"].append('Bravo '+nom+" vous êtes dès à present inscrit! Ceci est votre DashBoard")
			updateuserdatas()
		return render_template("default/index.html",datas=locals(),myapp = myapp)
	else :
		return render_template("default/inscriptions.html",datas=locals(),myapp = myapp)
		
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
			return render_template("default/index.html",datas=locals(),myapp = myapp)
	return render_template("default/connexion.html",datas=locals(),myapp = myapp)

@webapp.route('/list/widgets',methods=['POST'])
@login_required
def list_user_widget():
	user = request.form.get("user")
	toreturn =json.dumps(myapp.users[user]["widgets"])
	return(Response(response=toreturn,status=200,mimetype="application/json"))

@webapp.route('/chatbot',methods=["POST"])
@login_required
def chatbot_request():
	text = request.form.get("text")
	q = chatbot.question(text)
	q.load_user(session["utilisateur"])
	q.load_plugins(["default"])
	try :
		r = q.json()
		return(Response(response=r,status=200,mimetype="application/json"))
	except Exception as e :
		print("\nUne erreur est survenu lors d'une requette au chatbot")
		print("----------------------------\n",e,"\n----------------------------\n")
		return(Response(response=json.dumps("ERREUR"),status=200,mimetype="application/json"))

@webapp.route('/widgets')
@login_required
def widgets():
	return render_template("default/widgets.html",datas=locals(),myapp = myapp)
	
@webapp.route('/active/<type>/<what>')
@login_required
def active(type,what):
	if type == "widget" :
		settings = load_datas("settings")
		settings[session["utilisateur"]]["widgets"].append(what)
		myapp.users[session["utilisateur"]]["widgets"].append(what)
		update_datas(settings,"settings")
		toreturn =json.dumps("ok")
		return(Response(response=toreturn,status=200,mimetype="application/json"))
	
	if type == "application":
		settings = load_datas("settings")
		settings[session["utilisateur"]]["actived_apps"].append(what)
		update_datas(settings,"settings")
		toreturn =json.dumps("ok")
		#loadsystemdatas()
		updateuserdatas()
		return(Response(response=toreturn,status=200,mimetype="application/json"))
		
@webapp.route('/desactive/<type>/<what>')
@login_required
def desactive(type,what):
	if type == "widget" :
		settings = load_datas("settings")
		settings[session["utilisateur"]]["widgets"].remove(what)
		myapp.users[session["utilisateur"]]["widgets"].remove(what)
		update_datas(settings,"settings")
		toreturn =json.dumps("ok")
		return(Response(response=toreturn,status=200,mimetype="application/json"))
		
	if type == "application" :
		manifest = json.loads(open("apps/"+what+"/manifest.json").read())
		settings = load_datas("settings")
		settings[session["utilisateur"]]["actived_apps"].remove(what)
		del myapp.users[session["utilisateur"]]["apps"][manifest["displayName"]]
		for widget in manifest["widgets"]:
			if widget.replace("/","%2F") in myapp.users[session["utilisateur"]]["widgets"] : myapp.users[session["utilisateur"]]["widgets"].remove(widget.replace("/","%2F"))
		update_datas(settings,"settings")
		toreturn =json.dumps("ok")
		updateuserdatas()
		return(Response(response=toreturn,status=200,mimetype="application/json"))
		
@webapp.route('/logout')
def deconnexion():
	message = {}
	if session.get("utilisateur"):
		del(session["utilisateur"])
		message["succes"] =['Vous avez été deconnecté']
	else:
		message["error"] =['Vous n\'étiez pas connecté']
	return render_template("default/connexion.html",datas=locals(),myapp = myapp)


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
	myapp.__init__()
	for user in myapp.settings:
		for app in myapp.settings[user]["actived_apps"]:
			dir = app
			if os.path.isdir("apps/"+dir):
				manifest = json.loads(open("apps/"+dir+"/manifest.json").read())
				if manifest["urls"].get("menu"):
					myapp.users[user]["menu"].update(manifest["urls"]["menu"])
					for url in manifest["urls"]["menu"] :
						myapp.users[user]["urls"].append(manifest["urls"]["menu"][url])
				myapp.users[user]["apps"].update({manifest["displayName"]:manifest})
				
			else :
				print ("L'application '"+dir+"' n'éxiste pas !")
        

if "run" in argv:
    loadsystemdatas()
    updateuserdatas()
    myapp.start()
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
    
if "installapp" in argv :
	try:
		dir = argv[argv.index("installapp")+1]
	except IndexError :
		print("Quel est le chemin de votre packet ?")
		dir = input(">")
	if os.path.isdir(dir):
		if os.path.isfile(dir+"/"+"manifest.json"):
			print("Lecture du manifest...")
			packetmanifest = json.loads(open(dir+"/"+"manifest.json").read())
			print("Description: "+packetmanifest["description"])
			print("V:"+packetmanifest["version"])
			print ("Voulez vous vraiment installer cette application ?")
			while 1 : 
				yesornot = input("y/n>")
				if  yesornot == "y":
					print("Déplacement du packet")
					os.system("mv "+dir+" apps")
					packetfiles = os.listdir("apps/"+packetmanifest["name"])
					for element in packetfiles :
						elementapppath = "apps/"+packetmanifest["name"]+"/"+element
						print("Traitement de:",elementapppath)
						if os.path.isdir(elementapppath) and os.path.isdir(element):
							print("Déplacement de "+elementapppath)
							os.system("mv "+elementapppath+" "+element+"/apps")
					sys = load_datas("settings")
					if not packetmanifest["name"] in sys["sys"]["installed_apps"]:
						sys["sys"]["installed_apps"].append(packetmanifest["name"])
						sys["sys"]["widgets"].extend(packetmanifest.get("widgets",[]))
						update_datas(sys,"settings")
						print ("\n******** L'application a été installée ********")
					else:
						print ("\n******** L'application a déja été installée ********")
					break
				elif yesornot == "n":print("\n******** L'instalation a été anulée ********");break
		else:print("/!\ Le fichier manifest n'existe pas")
	else:print("/!\ Ce packet n'existe pas")
	
if "creatapp" in argv:
	try:
		name = argv[argv.index("creatapp")+1]
	except IndexError :
		name = input("Quel est le nom que voulez-vous appliquer à votre packet ?\n>")
	sys = load_datas("settings")
	if not name in sys["sys"]["installed_apps"]:
		description =input("Quel est le but de votre application?\n>")
		license = input("Quel license choisissez vous pour cette application?\n>")
		displayName = input("Quel nom doit être affiché?\n>")
		author = input("Qui êtes vous?\n>")
		manifest = {"name": name,"version": "0.1","description": description,"license": license,"displayName": displayName,"author": author,"datas": [],"templates": ["index.html"],"urls":{"menu":{displayName:"/"+name},"api":[]},"widgets":[]}
		print("Création de l'application (préinstallée)...")
		print("Pour exporter votre application une fois finie executée: exportapp "+name)
		os.system("mkdir apps/"+name)
		open("apps/"+name+"/manifest.json","w").write(json.dumps(manifest,indent=4,ensure_ascii=False))
		print("Le fichier apps/"+name+"/manifest.json de votre packet a été créé.")
		open("apps/"+name+"/"+name+".py","w").write("""
 
@webapp.route("/{name}")
@login_required
def index_{name}():
	'''
	Votre code
	'''
	return render_template("apps/{name}/index.html",datas=locals(),myapp=myapp)
		""".format(name=name))
		print("Le fichier apps/"+name+"/"+name+".py de votre packet a été créé.")
		os.system("mkdir templates/apps/"+name)
		open("templates/apps/"+name+"/index.html","w").write("""{% extends "default/design.html" %}{% block title %}"""+displayName+"""{% endblock %}
{% block content %}
	<div class="container">
		<h1>"""+displayName+""""</h1>
	</div>
{% endblock %}
	""")
		print("Le fichier templates/apps/"+name+"/index.html a été créé")
		print("L'utilisateur sys peux y acceder")
		sys["sys"]["installed_apps"].append(name)
		sys["sys"]["actived_apps"].append(name)
		update_datas(sys,"settings")
		print("Création de l'application terminée")
	else:
		print("Cette application éxiste déja")
	
if "exportapp" in argv:
	try:
		name = argv[argv.index("exportapp")+1]
	except IndexError :
		name = input("Quel est le nom de l'application à exporter ?\n>")
	try:
		path = argv[argv.index("exportapp")+2]
	except IndexError :
		path = input("Où exporter l'application ?\n>")
	if os.path.isdir(path):
		if os.path.isdir("apps/"+name):
			print("Exportation de "+name+" dans "+path+" ...")
			os.system("mkdir "+path+"/"+name+" && cp -r apps/"+name+" "+path+"/")
			dirs = ["datas/apps/","static/default/apps/","templates/apps/"]
			for dir in dirs :
				if os.path.isdir(dir+name):
					print("Création de "+path+"/"+name+"/"+dir.split("/")[0])
					print("Copie récursif des fichiers contenus dans "+dir+name)
					os.system("cp -r "+dir+name+" "+path+"/"+name+"/"+dir.split("/")[0])
			print("L'application a été exportée")
		else:
			print("/!\ L'application que vous essayez d'exporter n'existe pas.")
	else :
		while 1:
			r = input("/!\ Le chemin indiqué n'existe pas.\nVoulez le créer ? [y/n]\n>")
			if r == "y":
				os.system("mkdir "+path)
				print("Relancez la commande pour procéder à l'instalation.")
				break
			elif r == "n":
				print("Exportation annulée.")
				break