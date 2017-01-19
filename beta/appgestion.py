if "installapp" in argv:
    try:
        dir = argv[argv.index("installapp") + 1]
    except IndexError:
        print("Quel est le chemin de votre packet ?")
        dir = input(">")
    if os.path.isdir(dir):
        if os.path.isfile(dir + "/manifest.json"):
            print("Lecture du manifest...")
            packetmanifest = json.loads(
                open(dir + "/" + "manifest.json").read()
            )
            print("Description: " + packetmanifest["description"])
            print("V:" + packetmanifest["version"])
            print("Voulez vous vraiment installer cette application ?")
            while 1:
                yesornot = input("y/n>")
                if yesornot == "y":
                    print("Déplacement du packet")
                    os.system("mv " + dir + " apps")
                    packetfiles = os.listdir("apps/" + packetmanifest["name"])
                    for element in packetfiles:
                        elementapppath = "apps/" + packetmanifest["name"] + "/" + element
                        print("Traitement de:", elementapppath)
                        if os.path.isdir(elementapppath) and os.path.isdir(element):
                            print("Déplacement de " + elementapppath)
                            os.system("mv -v " + elementapppath+"/* " + element + "/apps")
                            os.system("rm " + elementapppath)
                    sys = load_datas( "settings")
                    if not packetmanifest["name"] in sys["sys"]["installed_apps"]:
                        sys["sys"]["installed_apps"].append(
                            packetmanifest["name"])
                        sys["sys"]["widgets"].extend(
                            packetmanifest.get("widgets", []))
                        update_datas(sys, "settings")
                        print("\n******** L'application a été installée ********")
                    else:
                        print(
                            "\n******** L'application a déja été installée ********")
                    break
                elif yesornot == "n":
                    print("\n******** L'instalation a été anulée ********")
                    break
        else:
            print("/!\ Le fichier manifest n'existe pas")
    else:
        print("/!\ Ce packet n'existe pas")

if "createapp" in argv:
    try:
        name = argv[argv.index("createapp") + 1]
    except IndexError:
        name = input(
            "Quel est le nom que voulez-vous appliquer à votre packet ?\n>")
    sys = load_datas("settings")
    if not name in sys["sys"]["installed_apps"]:
        description = input("Quel est le but de votre application?\n>")
        license = input(
            "Quel license choisissez vous pour cette application?\n>")
        displayName = input("Quel nom doit être affiché?\n>")
        author = input("Qui êtes vous?\n>")
        manifest = {"name": name, "version": "0.1", "description": description, "license": license, "displayName": displayName,
                    "author": author, "datas": [], "templates": ["index.html"], "urls": {"menu": {displayName: "/" + name}, "api": []}, "widgets": []}
        print("Création de l'application (préinstallée)...")
        print("Pour exporter votre application une fois finie executée: exportapp " + name)
        os.system("mkdir apps/" + name)
        open("apps/" + name + "/manifest.json",
             "w").write(json.dumps(manifest, indent=4, ensure_ascii=False))
        print("Le fichier apps/" + name +
              "/manifest.json de votre packet a été créé.")
        open("apps/" + name + "/" + name + ".py", "w").write("""

@webapp.route("/{name}")
@login_required
def index_{name}():
	'''
	Votre code
	'''
	return render_template("apps/{name}/index.html",datas=locals(),myapp=myapp)
		""".format(name=name))
        print("Le fichier apps/" + name + "/" +
              name + ".py de votre packet a été créé.")
        os.system("mkdir templates/apps/" + name)
        open("templates/apps/" + name + "/index.html", "w").write("""{% extends "default/design.html" %}{% block title %}""" + displayName + """{% endblock %}
{% block content %}
	<div class="container">
		<h1>""" + displayName + """</h1>
	</div>
{% endblock %}
	""")
        print("Le fichier templates/apps/" + name + "/index.html a été créé")
        print("L'utilisateur sys peux y acceder")
        sys["sys"]["installed_apps"].append(name)
        sys["sys"]["actived_apps"].append(name)
        update_datas(sys, "settings")
        print("Création de l'application terminée")
    else:
        print("Cette application éxiste déja")

if "exportapp" in argv:
    try:
        name = argv[argv.index("exportapp") + 1]
    except IndexError:
        name = input("Quel est le nom de l'application à exporter ?\n>")
    try:
        path = argv[argv.index("exportapp") + 2]
    except IndexError:
        path = input("Où exporter l'application ?\n>")
    if os.path.isdir(path):
        if os.path.isdir("apps/" + name):
            print("Exportation de " + name + " dans " + path + " ...")
            os.system("mkdir " + path + "/" + name +
                      " && cp -r apps/" + name + " " + path + "/")
            dirs = ["datas/apps/", "static/apps/", "templates/apps/"]
            for dir in dirs:
                if os.path.isdir(dir + name):
                    print("Création de " + path + "/" +
                          name + "/" + dir.split("/")[0])
                    print("Copie récursive des fichiers contenus dans " + dir + name)
                    os.system("cp -r " + dir + name + " " + path +
                              "/" + name + "/" + dir.split("/")[0])
            print("L'application a été exportée")
        else:
            print("/!\ L'application que vous essayez d'exporter n'existe pas.")
    else:
        while 1:
            r = input(
                "/!\ Le chemin indiqué n'existe pas.\nVoulez le créer ? [y/n]\n>")
            if r == "y":
                os.system("mkdir " + path)
                print("Relancez la commande pour procéder à l'instalation.")
                break
            elif r == "n":
                print("Exportation annulée.")
                break