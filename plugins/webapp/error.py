from flask import *

@webapp.errorhandler(404)
def page_not_found(e):
    return render_template('web/error.html',var=locals()), 404

@webapp.errorhandler(403)
def Forbidden(e):
    return render_template('web/error.html',var=locals()), 403

@webapp.errorhandler(500)
def Internal_Server_Error(e):
    return render_template('web/error.html',var=locals()), 500



