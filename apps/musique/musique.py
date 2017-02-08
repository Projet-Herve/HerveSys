global list_user_musique


def list_user_musique(user):
    message = {"error": []}
    if os.path.isdir("nas/" + user + '/'):
        if os.path.isdir("nas/" + user + "/musique"):
            files = os.listdir("nas/" + user + "/musique")
            audio_files = []
            for file in files:
                filename, file_extension = os.path.splitext(file)
                for i in load_datas("datas/extension.json"):
                    if i["extension"] == file_extension:
                        if "audio" in i["content-type"]:
                            audio_files.append(file)
                            break
        else:
            message["error"].append("Vous n'avez pas de dossier musique.")
    else:
        message["error"].append(
            "Vous n'avez pas de dossier personel pour le nas.")
    return audio_files

@webapp.route('/get/musique/<file>')
@login_required
def send_musique(file):
    user = session["utilisateur"]
    return send_from_directory("nas/" + user + "/musique", file)


@webapp.route('/widgets/vosmusiques')
@login_required
def widget_musique():
    list_ = "<h1><a href=\"/musique\">Vos musiques</a></h1>"
    listmusiques = list_user_musique(session["utilisateur"])
    for m in listmusiques:
        list_ += "<p href=\"#\" class=\"musique-item\" data-val=\"{m}\">{m}</p>".format(
            m=m)
    audio_files = tag("div", class_=["vosmusiques", "card", "white", "shadows"], contenu=tag(
        "div", class_=["content"], contenu=list_))
    return(Response(response=audio_files, status=200, mimetype="text/html"))


@webapp.route("/list/musique")
@login_required
def ajax_musique():
    audio_files = list_user_musique(session["utilisateur"])
    return(Response(response=json.dumps(audio_files), status=200, mimetype="application/json"))


@webapp.route("/musique")
@login_required
@need_app_active
def index_musique():
    return render_template("musique/templates/index.html")
