import json
from flask import *
from __main__ import login_required


@webapp.route('/notes', methods=["GET","POST"])
@login_required
def notes_index():
    s = myapp.settings()
    if not s[session["utilisateur"]]["datas"].get("notes"):
        s[session["utilisateur"]]["datas"]["notes"] = []
    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            s[session["utilisateur"]]["datas"]["notes"].append(
                {"id": len(s[session["utilisateur"]]["datas"]["notes"]) + 1, "text": note})
    update_datas(s,myapp.settings_file)
    return render_template("notes/templates/index.html",
                           datas={
                               "notes": s[session["utilisateur"]]["datas"]["notes"]
                           },
                           myapp=myapp)
