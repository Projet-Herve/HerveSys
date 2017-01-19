import json
from flask import *
from __main__ import login_required
import requests
from datetime import datetime


def get():
	try:
		todecode = requests.get("http://www.infoclimat.fr/public-api/gfs/json?_ll=48.85341,2.3488&_auth=BR9fSFYoXH5RfFFmVyFXflY%2BBzJaLAgvAHwCYQ9qUC1ROgNiUzMGYF4wVCkGKVJkByoEZwswBjYFbgF5WihfPgVvXzNWPVw7UT5RNFd4V3xWeAdmWnoILwBrAmcPfFAxUTEDYlMuBmZeMlQ0BihSZQc3BHsLKwY%2FBWIBblo3XzkFZ185Vj1cN1E9USxXeFdmVm0HZFowCGQAZgJiDzZQOlE1A2JTOQY3XjNUKAY%2BUmAHNQRlCzMGNwVkAWdaKF8jBR9fSFYoXH5RfFFmVyFXflYwBzlaMQ%3D%3D&_c=915375076ef306690039808fd98b183d").text
	except:
		todecode = {"error"}
	return(json.loads(todecode))

def getnow(joursdeplus=0):
	maintenant = datetime.now()
	heures = [1, 4, 7, 10, 13, 16, 19, 22]
	for heure in heures:
		if heure > 22 :
			if heure< maintenant.hour < heures[heures.index(heure)+1]:
				break
		else :
			heure = 22
	key = "{}-{}-{} {}:00:00".format(str(maintenant.year),str(maintenant.month) if len(str(maintenant.month)) ==2 else "0"+str(maintenant.month) ,str(maintenant.day+joursdeplus) if len(str(maintenant.day+joursdeplus)) ==2 else "0"+str(maintenant.day+joursdeplus),heure)
	return get()[key]

@webapp.route('/meteo')
def meteo():
	meteo = getnow()
	return render_template("web/apps/meteo/index.html",datas=locals(),myapp=myapp,getnow=getnow)

