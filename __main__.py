import sys
import os

from functools import wraps
from flask import *
from werkzeug.routing import BaseConverter
import jinja2

from time import sleep
import schedule
import threading
import hashlib
import pygeoip
from geopy.distance import vincenty
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
import requests
# import ngrok

from myhtml import tag
from datas import load_datas, update_datas
from jms import parse
from notify import *
import arduino
import chatbot

webapp = Flask(__name__)
webapp.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

webapp.jinja_loader = jinja2.ChoiceLoader(
    [webapp.jinja_loader, jinja2.FileSystemLoader(['apps/'])])


class RegexConverter(BaseConverter):

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


webapp.url_map.converters['regex'] = RegexConverter

script_path = os.path.dirname(os.path.realpath(__file__))


class DummySHA224Authorizer(DummyAuthorizer):

    def validate_authentication(self, username, password, handler):
        hash = hashlib.sha224(password.encode('utf8')).hexdigest()
        try:
            if self.user_table[username]['pwd'] != hash:
                raise KeyError
        except KeyError:
            raise AuthenticationFailed


class herveapp:

    def __init__(self):
        self.FTPAuthorizer = DummySHA224Authorizer()
        self.FTP_port = 21
        self.settings_file = "datas/settings.json"
        self.datas_dir = "datas/"
        self.ngrok = True
        self.ftp = True
        self.tests = False
        self.ngrok_location = "./"

    def settings(self):
        try:
            return load_datas(self.settings_file)
        except FileNotFoundError as e:
            print("Le fichier des settings n'existe pas")
            print(e)
            raise e

    def start_ngrok(self):
        os.system('{ngrok_location}ngrok start -config ~/.ngrok2/ngrok.yml -config=datas/ngrox.yml --all'.format(
            ngrok_location=self.ngrok_location
        ))

    def start_FTP(self):
        handler = FTPHandler
        handler.authorizer = self.FTPAuthorizer
        server = FTPServer((self.host, self.FTP_port), handler)
        server.serve_forever()

    def start_tests(self):
        for file in os.listdir('tests/'):
            test_src = open("tests/" + file)
            src = test_src.read()
            try:
                exec(src)
            except Exception as e:
                print("Un des test a échoué")
                print(e)
                print("Dans " + file)

    def start(self):
        self.forever_ = []
        self.users = dict()
        for user in self.settings():
            self.FTPAuthorizer.add_user(
                user, self.settings()[user]["profile"]["code"], "nas/"+user, perm='elradfmw')
            self.users[user] = {
                "apps": {},
                "menu": {"Accueil": "/", "Déconnexion": "/deconnexion", "Apps": "/apps", "Widgets": "/widgets"},
                "widgets": list(map(lambda x: x, self.settings()[user]["herve"]["widgets"])),
                "urls": []
                #"agenda" : agenda()
            }
            self.users[user].update(self.settings()[user])

        if self.tests is True:
            self.start_tests()

        def __forever():
            while True:
                for function in self.forever_:
                    function()

        def forschedule():
            while True:
                schedule.run_pending()
                sleep(1)

        threading.Thread(target=__forever).start()
        threading.Thread(target=forschedule).start()
        if self.ftp:
            threading.Thread(target=self.start_FTP).start()
        if self.ngrok:
            threading.Thread(target=self.start_ngrok).start()
        self.start_apps()
        self.updateuserdatas()

    def start_apps(self):
        for app in self.settings()["sys"]["herve"]["installed_apps"]:
            dir = app
            file = app + ".py"
            if os.path.isdir("apps/" + dir):
                app_src = open("apps/" + dir + "/" + file)
                src = app_src.read()
                try:
                    exec(src)
                except Exception as e:
                    print(
                        "\nUne erreur est survenu lors de l’exécution du module " + dir)
                    print("----------------------------\n", e,
                          "\n----------------------------\n")
            else:
                print("L'application '" + dir + "' n’existe pas !")

    def updateuserdatas(self):
        for user in self.settings():
            for app in self.settings()[user]["herve"]["actived_apps"]:
                dir = app
                if os.path.isdir("apps/" + dir):
                    manifest = json.loads(
                        open("apps/" + dir + "/manifest.json").read())
                    if manifest["urls"].get("menu"):
                        self.users[user]["menu"].update(
                            manifest["urls"]["menu"])
                        for url in manifest["urls"]["menu"]:
                            self.users[user]["urls"].append(
                                manifest["urls"]["menu"][url])
                    self.users[user]["apps"].update(
                        {manifest["displayName"]: manifest})

                else:
                    print("L'application '" + dir + "' n’existe pas !")

    # Décorateurs

    def forever(self, function):
        def decorator(function):
            try:
                self.forever_.append(function)
                return True
            except Exception as e:
                print("----------------------------\n", e,
                      "\n----------------------------\n")
                return False
        return decorator(function)

    def in_thread(self, function):
        threading.Thread(target=function).start()


myapp = herveapp()

# Décorteurs


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
            return render_template("default/connexion.html", datas=locals(), myapp=myapp)
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
        if not requesturl in myapp.users[session["utilisateur"]]["urls"]:
            return redirect("/", code=302)
        return f(*args, **kwargs)
    return decorated

# Erreurs


@webapp.errorhandler(404)
def page_not_found(e):
    return render_template('default/error.html', datas=locals(), myapp=myapp)


@webapp.errorhandler(403)
def Forbidden(e):
    return render_template('default/error.html', datas=locals(), myapp=myapp)


@webapp.errorhandler(500)
def Internal_Server_Error(e):
    return render_template('default/error.html', datas=locals(), myapp=myapp)

# Static Files


@webapp.route('/static/<app>/<path:filename>')
def custom_static(app, filename):
    if app != "default":
        return send_from_directory("apps/" + app + "/static/", filename)
    else:
        return send_from_directory("static/default/", filename)


@webapp.route('/static/<regex("[a-zA-Z//]*"):app>/jms/<script>')
def jms_page(app, script):
    try:
        if app != "default":
            return Response(response=parse(open("apps/" + app + "/static/jms/" + script, 'r').read()), status=200, mimetype="text/javascript")
        else:
            return Response(response=parse(open("static/default/jms/" + script, 'r').read()), status=200, mimetype="text/javascript")

    except:
        print("fichier '" + script + "' introuvable")
        return Response(response="console.log('Fichier jms non trouvé ! (Fichier : " + script + ") ; Ou erreur interne du au serveur :/');", status=404, mimetype="text/javascript")

# Vues simples


@webapp.route('/apps', methods=['GET'])
@login_required
def apps():
    return render_template("default/apps.html", datas=locals(), myapp=myapp)


@webapp.route('/index')
@webapp.route('/')
@login_required
def index():
    return render_template("default/index.html", datas=locals(), myapp=myapp)


@webapp.route('/widgets')
@login_required
def widgets():
    return render_template("default/widgets.html", datas=locals(), myapp=myapp)


@webapp.route('/dashboard')
def dashboard():
    return render_template("default/dashboard.html", datas=locals(), myapp=myapp)

# Inscriptions Connexion Déconnexion


@webapp.route('/inscriptions', methods=['GET', 'POST'])
def inscriptions():
    datas = myapp.settings()
    if request.method == 'POST':
        nom = str(request.form.get('nom'))
        code1 = request.form.get('code1')
        code2 = request.form.get('code2')
        message = {"error": [], "succes": []}
        if not nom:
            message["error"].append('Veillez choisir un nom d\'utilistaur')
        if not code1:
            message["error"].append('Veillez choisir un code de securite')
        if not code2:
            message["error"].append('Veillez retapper votre code de securite')
        if code1 != code2:
            message["error"].append('Veillez entrer deux fois le meme code')
        if not message['error']:
            nouveauutilisateur = {
                "id": len(datas),
                "nom": nom,
                "code": hashlib.sha224(code1.encode('utf8')).hexdigest()
            }
            session['utilisateur'] = nom
            user = {
                nom: {
                    "profile": nouveauutilisateur,
                    "herve": {
                        "actived_apps": [],
                        "widgets": []
                    }
                }
            }
            os.makedirs("nas/" + nom)
            datas.update(user)
            myapp.users.update(user)
            update_datas(datas, myapp.settings_file)
            message["succes"].append(
                'Bravo ' + nom + " vous êtes dès à present inscrit! Ceci est votre DashBoard")
            myapp.updateuserdatas()
            return render_template("default/index.html", datas=locals(), myapp=myapp)
        else:
            return render_template("default/inscriptions.html", datas=locals(), myapp=myapp)
    else:
        return render_template("default/inscriptions.html", datas=locals(), myapp=myapp)


@webapp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if len(myapp.users) == 1:
        return redirect("/inscriptions", code=302)
    if request.method == "POST":
        message = {"error": [], "succes": []}
        if not request.form.get("nom"):
            message["error"].append(
                "Vous devez entrer votre nom d'utilisateur")
        if not request.form.get("code"):
            message["error"].append("Vous devez entrer votre code")
        if request.form.get("code") and request.form.get("nom"):
            if myapp.settings().get(request.form.get("nom")):
                if myapp.settings()[request.form.get("nom")]["profile"]["code"] == hashlib.sha224(request.form.get("code").encode('utf8')).hexdigest():
                    session["utilisateur"] = request.form.get("nom")
            if not session.get("utilisateur"):
                message["error"].append("Vous n'avez pas pu etre connecté")
            else:
                message["succes"].append("Vous etes connecté")
        if len(message["error"]) == 0:
            if request.form.get("json"):
                return(Response(response=json.dumps(locals()), status=200, mimetype="application/json"))
            else:
                return redirect(request.form.get("next"), code=302)
                # return render_template("default/index.html", datas=locals(),
                # myapp=myapp)
    return render_template("default/connexion.html", datas=locals(), myapp=myapp)


@webapp.route('/deconnexion')
def deconnexion():
    message = {}
    if session.get("utilisateur"):
        del(session["utilisateur"])
        message["succes"] = ['Vous avez été deconnecté']
    else:
        message["error"] = ['Vous n\'étiez pas connecté']
    return render_template("default/connexion.html", datas=locals(), myapp=myapp)


@webapp.route('/list/widgets', methods=['GET'])
@login_required
def list_user_widget():
    user = session["utilisateur"]
    toreturn = json.dumps(myapp.users[user]["herve"]["widgets"])
    return(Response(response=toreturn, status=200, mimetype="application/json"))


@webapp.route('/chatbot', methods=["GET"])
@login_required
def chatbot_request():
    text = request.args.get("text")
    settings = myapp.settings()
    settings[session["utilisateur"]]["herve"]["chatbot"][
        "history"].append({session["utilisateur"]: text})
    q = chatbot.question(text, settings_file=myapp.settings_file)
    q.load_user(session["utilisateur"])
    q.load_plugins(["default", "blagues"])
    # q.checkortho()
    try:
        r = q.json()
        settings[session["utilisateur"]]["herve"]["chatbot"][
            "history"].append({"sys": r})
        update_datas(settings, myapp.settings_file)
        return(Response(response=r, status=200, mimetype="application/json"))
    except Exception as e:
        print("\nUne erreur est survenu lors d'une requette au chatbot")
        print("----------------------------\n", e,
              "\n----------------------------\n")
        raise e
        return(Response(response='{"erreur"}', status=200, mimetype="application/json"))


@webapp.route('/active/widget')
@login_required
def active_widget():
    what = request.args.get("what")
    settings = myapp.settings()
    settings[session["utilisateur"]]["herve"]["widgets"].append(what)
    myapp.users[session["utilisateur"]]["herve"]["widgets"].append(what)
    update_datas(settings, myapp.settings_file)
    toreturn = json.dumps("ok")
    return(Response(response=toreturn, status=200, mimetype="application/json"))

@webapp.route('/desactive/widget')
@login_required
def desactive_widget():
    what = request.args.get("what")
    settings = myapp.settings()
    settings[session["utilisateur"]]["herve"]["widgets"].remove(what)
    myapp.users[session["utilisateur"]]["herve"]["widgets"].remove(what)
    update_datas(settings, myapp.settings_file)
    toreturn = json.dumps("ok")
    return(Response(response=toreturn, status=200, mimetype="application/json"))


@webapp.route('/active/app/<what>')
@login_required
def active_app(what):
    settings = myapp.settings()
    settings[session["utilisateur"]]["herve"]["actived_apps"].append(what)
    update_datas(settings, myapp.settings_file)
    toreturn = json.dumps("ok")
    myapp.updateuserdatas()
    return render_template("default/apps.html", datas=locals(), myapp=myapp)


@webapp.route('/desactive/app/<what>')
@login_required
def desactive_app(what):
    manifest = json.loads(open("apps/" + what + "/manifest.json").read())
    settings = myapp.settings()
    settings[session["utilisateur"]]["herve"]["actived_apps"].remove(what)
    del myapp.users[session["utilisateur"]]["apps"][manifest["displayName"]]
    for widget in manifest["widgets"]:
        if widget in myapp.users[session["utilisateur"]]["herve"]["widgets"]:
            myapp.users[session["utilisateur"]]["herve"][
                "widgets"].remove(widget)
    update_datas(settings, myapp.settings_file)
    toreturn = json.dumps("ok")
    myapp.updateuserdatas()
    return render_template("default/apps.html", datas=locals(), myapp=myapp)


@webapp.route('/localiser')
@login_required
def localiser():
    # MaxMind, GeoIP, minFraud, and related trademarks are the trademarks of
    # MaxMind, Inc.
    message = {"error": [], "message": []}
    ip = request.args.get("ip")
    rawdata = pygeoip.GeoIP('datas/GeoLiteCity.dat')
    dataclient = rawdata.record_by_name(ip)
    if dataclient:
        message["result"] = dataclient
    else:
        message["error"].append("Aucune IP n'a été renseignée")
    return(Response(response=json.dumps(message), status=200, mimetype="application/json"))


@webapp.route('/ajax/<regex(".*"):url>')
@login_required
def ajax(url):
    try:
        print(url)
        return Response(response=requests.get(url).text, status=200)
    except Exception as e:
        print(e)
        pass

argvs = dict()
for argv in sys.argv[1:]:
    if argv not in argvs.values():
        with_val = False
        name = argv
        if argv[0] == "-":
            name = argv[1:]
            with_val = True

        if with_val is True:
            val = sys.argv[sys.argv.index(argv) + 1]
            sys.argv.remove(val)
            try:
                val = int(val)
            except ValueError as e:
                pass
            except Exception as e:
                raise e
            if val == "True" or val == "true":
                val = True
            if val == "False" or val == "false":
                val = False

        else:
            val = None
        argvs[name] = val

if "run" in argvs:
    start_arguments = {
        "host": "0.0.0.0",
        "port": 8080,
    }
    start_arguments.update(argvs)
    myapp.__dict__.update(start_arguments)
    myapp.start()
    webapp.run(host=myapp.host,
               port=myapp.port,
               debug=True,
               use_reloader=False)


if "createapp" in argvs:
    app = dict()
    app["displayName"] = input("Choisissez un nom d'affichage: \n>")
    app["name"] = input("Choisissez un nom simple pour votre application: \n>")
    app["version"] = 0.1
    app["description"] = input("Choisissez une description: \n>",)
    app["licence"] = input("Choisissez une licence: \n>")
    app["urls"] = {"menu":{app["displayName"],"/"+app["name"]}}
    manifest = json.dumps(app)
    os.makedirs("tmp/{name}/".format(**app), exist_ok=True)
    open(
        "tmp/{name}/manifest.json".format(name=app["name"]), "w").write(manifest)
    files = open("datas/new_app.json", "r").read()
    files = files.format(**app)
    files = json.loads(files)
    for file in files:
        os.makedirs(
            "tmp/{name}/".format(**app)+os.path.dirname(file), exist_ok=True)
        open("tmp/{name}/".format(**app)+file, "w").write(files[file])
    print("L'application a été crée dans tmp/")


if "installapp" in argvs:
    myapp.__dict__.update(argvs)
    app_nexiste_pas = "L'application n'existe pas"
    if not argvs.get("path"):
        path = input("Choisissez le chemin de l'application:\n>")
    else:
        path = argvs["path"]

    if os.path.isdir(path):
        if os.path.isfile(path + "manifest.json"):
            try:
                manifest = load_datas(path + "manifest.json", "r")
                s = load_datas(myapp.settings_file)
                if manifest["name"] in s["sys"]["herve"]["installed_apps"]:
                    print("L'application a déjà été installée")
                else:
                    os.sytem("cp -r "+path+" apps/")
                    s["sys"]["herve"]["installed_apps"].append(
                        manifest["name"])
                    update_datas(s, myapp.settings_file)
                    print("L'application a été installée")
            except Exception as e:
                ptin(e)
        else:
            print(app_nexiste_pas)
    else:
        print(app_nexiste_pas)
