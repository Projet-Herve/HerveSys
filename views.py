"""
	Fichier issu de la précédente version ne pas prendre en compte
"""








#####################
### Django import ###
#####################

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms

#################
### My import ###
#################

import datetime
from importlib.machinery import SourceFileLoader
from threading import Thread
import threading
import json
import requests
import time
import urllib.request
import urllib.parse
import os
import webbrowser
import sys
import RPi.GPIO as GPIO
import base64
import urllib
import subprocess
########################
###  Autres Projets  ###
########################

# IMPORT Searx_1_0
Searx_1_0 = SourceFileLoader("", "../Searx-1.0/__init__.py").load_module()
# IMPORT Probabilite_To_Click
ptc = SourceFileLoader("", "../Probabilite_To_Click/__init__.py").load_module()
# IMPORT Downloader
downloader = SourceFileLoader("", "../downloader/__init__.py").load_module()
# IMPORT Herve-Basique-IA-1.0
ia = SourceFileLoader("", "../Herve-Basique-IA/brain2.py").load_module()
# IMPORT Reseau
reseau = SourceFileLoader("", "../Reseau/__init__.py").load_module()
# IMPORT Maison-1.0
maison = SourceFileLoader("", "../Maison-1.0/__init__.py").load_module()
# IMPORT ATJOB-1.0
atjob = SourceFileLoader("", "../Atjob-1.0/__init__.py").load_module()
# Import Article-Extractor
article_extractor = SourceFileLoader("","../Article-Extractor/__init__.py").load_module()
# Import Arduino_Python
arduino = SourceFileLoader("","../Arduino-Python-1.0/arduino.py").load_module()

##########################
###  GLOBAL VARIABLES  ###
##########################
global donnee
global cloudfiles
global data_users
global liste_menu
global meteo_va
global meteoresult
global actus
global pages
global etat_internet
global etat_internet_text
global pieces
global action
global meteoresult
global actus
global meteoville
global pages
global serveur_url
global dossier_script
global preferences
global script
global musiqueetat
donnee = []
script = 'run'
serveur_url = sys.argv[2]
dossier_script = os.path.abspath(os.path.dirname(sys.argv[0]))

##############
###  init  ###
##############
#os.popen('sudo /usr/bin/setterm -blank 0 -powerdown off')

###########################
###  Fonctions / Class  ###
###########################
def cachedelay(date,delay=5):
	time  = datetime.datetime.now() - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
	delay = datetime.timedelta(minutes=delay)
	if time < delay:
		return True
	else:
		return False

def musiqueetat():
	etat = subprocess.Popen(['mocp','-Q','%state:/%file:/%title:/%artist:/%song:/%album:/%tt:/%tl:/%ts:/%ct:/%cs:/%b:/%r'], stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split(':/')
	finaletat = {}
	
	"""
	data_keys = ['state', 'file', 'title', 'artist', 'album', 'song', ...]

	mocp_args = '%' + ':/%'.join(data_keys)
	data_values = subprocess.Popen(['mocp', '-Q', args], stdout=subprocess.PIPE).communication...

	data = zip(data_keys, data_values)
	"""


	if 'FATAL_ERROR' in etat[0] or '' == etat[0]:
		finaletat['state'] = 'STOP'
	else :
		finaletat['state']= etat[0]
		finaletat['file']= etat[1]
		finaletat['title']= etat[2]
		finaletat['artist']= etat[3]
		finaletat['song']= etat[4]
		finaletat['album']= etat[5]
		finaletat['tt']= etat[6]
		finaletat['tl']= etat[7]
		finaletat['ts']= etat[8]
		finaletat['ct']= etat[9]
		finaletat['cs']= etat[10]
		finaletat['b']= etat[11]
		finaletat['r']= etat[12]
		try :
			if int(finaletat['ts']) > 1 and int(finaletat['cs']) > 1:
				finaletat['p'] = str((int(finaletat['cs']) / int(finaletat['ts']) * 100).__round__(5)).replace(',','.')
			else :
				finaletat['p'] = 0
		except:
			finaletat['p'] = 0
	return finaletat


def log(text,type):
	date = str(datetime.datetime.now())
	print('[' + date + ']['+type+'] - {}'.format(text))
	newlog = {'date':date,'objet':text,'type':type}
	log = json_to_variable('datas/log.json')
	log.append(newlog)
	variable_to_json(log,'datas/log.json')

def mail(to,subject,text):
    templatefile = open('templates/mail/default.html','r')
    template = templatefile.read()
    templatefile.close()
    log("envoie d'un mail a {}".format(to),'mail')
    return requests.post(
        "https://api.mailgun.net/v3/sandbox12261d80727f44c489ee4e90d2f8c3e8.mailgun.org/messages",
        auth=("api", preferences['mail']['api_key']),
        data={"from": preferences['mail']['from'],
              "to": to,
              "subject": subject,
              "html": template.format(objet=subject,contenu=text)})

def fichier_vers_base64(nom_fichier):
		with open(nom_fichier, "rb") as image_file:
			encoded_string = base64.b64encode(image_file.read())
			return encoded_string

def update_menu(id):
	with open('datas/menu.json', 'r+') as f:
		page = {}
		pages_2 = json.load(f)
		z = -1
		while z != len(pages)-1:
			z = z + 1
			if int(pages_2[z]['id']) == id:
				pages_2[z]['order']= int(pages_2[z]['order'])+1
				break
		pages_2 = json.dumps(pages_2,indent=4,ensure_ascii=False)
		f.seek(0)
		f.write(pages_2)
		f.truncate()

def json_maison():
	with open('datas/maison.json','r') as f :
			return json.load(f)
			f.seek(0)

def json_action():
	with open('datas/action.json','r') as f :
			return json.load(f)
			f.seekc

URL_SUBMIT='http://www.meteofrance.com/recherche/resultats'


def say(text):
	log('synthese du text "{}"'.format(text),'TTS')
	os.system('espeak "{}" -vfr-12 -s 200 -p 40'.format(text))
	#~ text = urllib.parse.urlencode({'q':text})
	#~ os.system('mpg321 "http://translate.google.com/translate_tts?tl=fr&client=tw-ob&{}"'.format(text))
	#print('mpg321 "http://translate.google.com/translate_tts?tl=fr&client=tw-ob&q={}"'.format(text))

global donnee
donnee = []
def meteo(meteoville):
	global URL_SUBMIT
	payload={ 'query': meteoville, 'facet': 'previsions',}
	r=requests.post(URL_SUBMIT, data=payload)
	reponse=r.text
	bmin=reponse.find('bloc-day-summary active')
	reponse=reponse[bmin:]
	bmax=reponse.find('</article>')
	reponse=reponse[:bmax]
	infos=list()
	for m in range(3):
		bmin=reponse.find('<span')
		reponse=reponse[bmin+1:]
		bmax=reponse.find('</span>')
		try:
			infos.append((reponse[:bmax].split('>')[1]).encode('utf-8'))
			reponse=reponse[bmax:]
		except IndexError:
			infos=False
			break

	'''
	infos[0] : température minimale.
	infos[1] : température maximale.
	infos[2] : tendance (ex: averses, nuageux, etc...)
	'''
	return infos

def searx(req):
	return (Searx_1_0.request(req))

def variable_to_json(variable,file):
	try :
		open(file,'w').write(json.dumps(variable,indent=4))
		return True
	except :
		return False

def json_to_variable(file):
	with open(file, 'r+') as f:
		return json.load(f)


def doaction (id):
	Qreactions = json_to_variable('datas/qreation.json') 
	for i in Qreactions :
		if i['id'] == int(id) :
			exec(i['python'])
			os.system(i['bash'])
			


def actus_blog():
	actus_json=requests.get('http://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=10&q=http://herveprojet.hol.es/blog/category/info/feed/')
	try :
		actus = json.loads(actus_json.text)
		actus = actus["responseData"]["feed"]["entries"]
	except :
		actus = ['Il est impossible d\'acceder aux actus Hervé','']
	return actus

def menu():
	with open('datas/menu.json', 'r+') as f:
		pages = json.load(f)
		f.seek(0)
		return pages

def serveur():
	with open('datas/serveur.json', 'r+') as f:
		pages = json.load(f)
		f.seek(0)
		return pages

#################
### VARIABLES ###
#################

def variable():
	global donnee
	global cloudfiles
	global data_users
	global liste_menu
	global meteo_va
	global meteoresult
	global actus
	global pages
	global etat_internet
	global etat_internet_text
	global pieces
	global action
	global meteoresult
	global actus
	global meteoville
	global pages
	global serveur_url
	global dossier_script
	global preferences
	global script
##############
###  MENU  ###
##############
	pages = menu()
	for i in pages: i['order'] = int(i['order'])

#############
###  NOW  ###
#############
	def liste():
		ordered= ptc.quick_sort(pages)
		ordered=ordered[::-1] # On inverse la liste
		#ordered=ordered[:5]  # 5 premier resultats
		return ordered
	liste_menu = liste()



#############
### CLOUD ###
#############
	cloudfilesliste = os.listdir('static/default/cloud/')
	cloudfiles = []
	def typefile (i,type_,liste):

		for y in liste:
			if i.split('.')[-1] == y:
				type_file = type_
				if type_file :
					cloudfiles.append({'Files' : i, 'extention' :i.split('.')[-1],'type' : type_file})
			elif i.split('.')[-2:-1] == y:
				#print( i.split('.')[-2:-1])
				type_file = type_
				if type_file :
					cloudfiles.append({'Files' : i, 'extention' :i.split('.')[-2:-1],'type' : type_file})

	for i in cloudfilesliste :
		po = False
		typefile(i,'musique',['aac','mp3','wav','midi','aiff','org'])
		typefile(i,'text',['txt'])
		typefile(i,'video',['mp4','ogg','msmp4','avi'])
		typefile(i,'web',['html','css','php','js','htm','sql'])
		typefile(i,'python',['py','pyc','pyo','pyu','pyw'])
		typefile(i,'archives',['zip','rar','tar.gz'])
		typefile(i,'C/C++',['c','h','cpp','hpp'])
		for y in cloudfiles :
			if  i == y['Files'] :
				po = True
		if po is not True:
			cloudfiles.append({"Files" : i, "extention" :i.split('.')[-1],"type" : "inconnu"})
	donnee.append({"cloudfiles" : cloudfiles})


###################
### Préferences ###
###################

	with open('datas/preferences.json', 'r+') as file:
		global preferences
		preferences = json.load(file)
		preferences['serveur_url'] = serveur_url
		for serveur in preferences['serveur']:
			serveur['lancement'] = serveur['lancement'].format(serveur_url = preferences['serveur_url'][:-5])
			serveur['acces'] = serveur['acces'].format(serveur_url = preferences['serveur_url'][:-5])




#############
### METEO ###
#############

	logs = json_to_variable('datas/log.json')
	a = 0
	nbitem = 0
	if len(logs) != 0 :
		for item in logs:

			if item['type'] == 'meteo' :
				nbitem = nbitem+1
				if cachedelay(item['date'],delay=5) == False :
					a = a +1


	#print (str(nbitem)+' '+str(a))
	if a == nbitem:
		log('update','meteo')
		meteoresult=meteo(preferences['ville_meteo'])
		if meteoresult != False:
			for indice,i in enumerate(meteoresult):
				meteoresult[indice]=i.decode()
		else:

			meteoresult = "Météo indisponible :/"
		if meteoresult != "Météo indisponible :/":
			meteoresult = {"minimal":meteoresult[0],"maximale":meteoresult[1],"tendance":meteoresult[2]}
			donnee.append({"meteo":meteoresult})
		else :
			meteoresult = {"minimal":"Météo indisponible :/","maximale":"Météo indisponible :/","tendance":"Météo indisponible :/"}
			donnee.append({"meteo":meteoresult})



#############
### ACTUS ###
#############

	actus = actus_blog()
	donnee.append({'herve-actus':actus})


################
### INTERNET ###
################

	#etat_internet= reseau.internet(reactive=False)
	etat_internet = True
	if etat_internet == True :
		etat_internet_text='Disponible'
	else :
		etat_internet_text = 'Controle parental actif (Freebox)'


##############
### Maison ###
##############
	pieces = json_maison()

##############
### action ###
##############
	action = json_action()

################################
### FIN VARIABLES GLOBAL (2) ###
################################


def asynchrone():
	while True:
		time.sleep(1)
		variable()


###############
### Serveur ###
###############


#~ def start_serveur(serveur_name):
	#~ for serveur in preferences['serveur']:
		#~ if serveur['nom'] == serveur_name :
			#~ exec("def start_serveur_{serveur_name}():\t	os.system(\"{lancement}\")\n{serveur_name} = threading.Thread( group=None, target=start_serveur_{serveur_name}, name=None)\n{serveur_name}.start()".format(serveur_name=serveur['nom'],lancement=serveur['lancement']))
#~
#~
#~ def stop_serveur(serveur_name):
	#~ pass
	#~
###########
### Tap	###
###########
def tap():
	con = arduino.connect()
	arduino.write('action led on',con)
	arduino.read(con)
	time.sleep(0.01)
	arduino.write('action led off',con)
	arduino.read(con)
	while script == 'run':
		commandes = json_to_variable('datas/commandes-arduino.json')
		returned = arduino.read(con)
		returned = str(returned[2:-5])
		returned = json.loads(returned)
		returnedcode = "CODE INVALIDE"
		try:
			time1 = (returned['values']['time1']/1000).__round__(0)
			time2 = (returned['values']['time2']/1000).__round__(0)
			etendue = time2 -time1

			if etendue == 0 :
				# On est dans le cas ou les deux intevales sont de meme durée
				if time1 >= 2 :
					returnedcode='LONG LONG'
				elif time1  <= 2 :
					returnedcode='COURT COURT'
					requests.get('http://'+serveur_url+'/dashboard_new/')

			elif etendue < 0:
				# On est dans le cas ou les deux intervales ne sont pas de meme durée
				if time1 >= 2:
					returnedcode='LONG COURT'
			elif etendue > 0:
				# On est dans le cas ou les deux intervales ne sont pas de meme durée
				if time1 <= 2:
					returnedcode='COURT LONG'
			else :
				# On est dans tous les autres cas
				returnedcode = 'CODE INVALIDE'
			try :
				exec(commandes[returnedcode]['python'])
			except:
				say('impossible de lancer le code python')
			os.system(commandes[returnedcode]['commande'])
			log(returnedcode,'Arduino')

		except :
			pass
			#log(returned['message'])

	arduino.deconnect()


say("Début du démarage d'Hervé")
asynchrone = threading.Thread(None,asynchrone)
asynchrone.start()
tap = threading.Thread(None,tap)
tap.start()
time.sleep(2)



################
###  Pages   ###
################

################
### ChatBot  ###
################

def chatbot (request):
	chatbot = ia.chatbot(config={'learn':False,'learn_file':'datas/learn.py','debug':False})
	if request.GET.get("text"):
		result = chatbot.init(msg=request.GET.get("text"))[0]
		return HttpResponse(result, content_type="text/plain")
	else:
		return HttpResponse("Vous devez definir 'text'", content_type="text/plain")

#######################
### Articles Reader ###
#######################

def articlereader (request):

	if request.GET.get("url"):
		article = article_extractor.init(url=request.GET.get("url"),file='../Article-Extractor/website.json')
		say(article['contenu']['nohtml'])
		return HttpResponse(article['contenu']['nohtml'], content_type="text/plain")

	else:
		return HttpResponse("Vous devez definir 'url'", content_type="text/plain")

###########
### SAY ###
###########

def sayfromweb (request):

	if request.GET.get("text"):
		saytext(request.GET.get("text"))
		#mail('julesmichaelmail@gmail.com','test','Bonjour Monsieur')
		return HttpResponse('ok', content_type="text/plain")
	else:
		return HttpResponse("Vous devez definir 'text'", content_type="text/plain")

##########################################
### SPECIAL PAGE WEB / DASHBOARD / HMS ###
##########################################

def dashboard(request):

	return render(request, 'html/dashboard/index.html',{'actus': actus,'internet':etat_internet_text,'action':action})

def open_dashboard(request):

	webbrowser.open('http://'+serveur_url+'/dashboard')
	return render(request, 'html/index.html', {'files':cloudfiles ,'menuliste':liste_menu})

def media_serveur(request):

	video_url = request.GET.get("video_url")
	return render(request, 'html/media_serveur.html', {"video_url":video_url})

def open_media_serveur(request):

	video_url = request.GET.get("video_url")
	url = 'http://'+serveur_url+'/media_serveur/?video_url='+video_url
	webbrowser.open(url)
	return render(request, 'html/index.html', {'files':cloudfiles ,'menuliste':liste_menu})


#################
### API Pages ###
#################

def api_meteo(request):

	return HttpResponse(json.dumps({"meteo":meteoresult},indent=4,ensure_ascii=False), content_type="application/json")


#################
### PAGES WEB ###
#################

def handle_uploaded_file(f):
		with open('name.txt', 'wb+') as destination:
				for chunk in f.chunks():
						destination.write(chunk)

@csrf_exempt
def upload_file(request):
		if request.method == 'POST':
				form = UploadFileForm(request.POST, request.FILES)
				if form.is_valid():
						handle_uploaded_file(request.FILES['file'])
						return HttpResponseRedirect('/')
		else:
				form = UploadFileForm()
		return render(request, 'upload.html', {'form': form})

@csrf_exempt
def api(request):

	with open('datas/api.json', 'r+') as f:
		with open('datas/commendes') as commendes:
			with open('datas/menu.json') as lm:
				lm = lm.read()

			commendes_content = commendes.read()
			json_data = donnee #json.dumps(donnee,ensure_ascii=False)
			f.seek(0)
			json_data = json.dumps(json_data,indent=4,ensure_ascii=False)
			json_data = str(json_data)
			json_data.replace("'", '"')
			json_data = json_data[:-1]+','+commendes_content+',"menu":'+lm+']'

			f.write(json_data)
			f.truncate()
	return HttpResponse(json_data, content_type="text/plain")
	#return render(request, 'json/api.json',{'donnee':json_data})
	#return JsonResponse(json_data, safe=False)

@csrf_exempt
def rechercherapide(request):

	if request.method == 'POST':
		return render(request, 'html/rechercherapide.html',{'resultats': json.loads(searx(request.POST.get("request"))),'menuliste':liste_menu})
	if request.method == 'GET':
		return render(request, 'html/rechercherapide.html',{'menuliste':liste_menu})

def actusweb(request):

	return render(request, 'html/actualites.html' , {'actus':actus,'menuliste':liste_menu})

def meteoweb(request):
	global meteoville
	if request.method == 'GET':

		return render(request, 'html/meteo.html', {'meteo':meteoresult , 'meteoville':preferences['ville_meteo'] ,'menuliste':liste_menu})
	if request.method == 'POST':

		if request.POST.get("meteoville") :
			meteovilleform  = request.POST.get("meteoville")
			meteoville = request.POST.get("meteoville")

			return render(request, 'html/meteo.html', {'meteo':meteoresult , 'meteoville':preferences['ville_meteo'] , 'meteovilleform':meteovilleform,'menuliste':liste_menu })

def meteoapi(request):
	global meteoville
	if request.method == 'GET':

		return render(request, 'html/meteoapi.html', {'meteo':meteoresult , 'meteoville':preferences['ville_meteo'],'menuliste':liste_menu})
	if request.method == 'POST':

		if request.POST.get("meteoville") :
			meteovilleform  = request.POST.get("meteoville")
			meteoville = request.POST.get("meteoville")

			return render(request, 'html/meteoapi.html', {'meteo':meteoresult , 'meteoville':preferences['ville_meteo'] , 'meteovilleform':meteovilleform,'menuliste':liste_menu})
			return render(request, 'html/meteoapi.html', {'meteo':meteoresult , 'meteoville':preferences['ville_meteo'] , 'meteovilleform':meteovilleform,'menuliste':liste_menu})

@csrf_exempt
def downloder(request):
	if request.method == 'GET':

		return render(request, 'html/downloader.html',{'menuliste':liste_menu})
	if request.method == 'POST':

		if request.POST.get("url") :
			url  = request.POST.get("url")

			#downloader.file_download(url)
			dwn1 = downloader.downloader(url)
			dwn1.start()
			return render(request, 'html/downloader.html', {'url':url,'menuliste':liste_menu})
			dwn1.join()

def filemodif(request):

	if  request.method == 'POST':
		if request.POST.get("modifiquation") :
			with open('static/default/cloud/'+request.POST.get("modifiquation")) as file:
				fileextention = request.POST.get("modifiquation").split('.')[-1]
				filecontent = file.read()
				return render(request,'html/modifiquation.html',{'files':cloudfiles,'filecontent':filecontent,'filename':request.POST.get("modifiquation"),'fileextention':fileextention,'menuliste':liste_menu})
		if request.POST.get("modif"):
			with open('static/default/cloud/'+request.POST.get("file"),'r+') as file:
				file.write(str(request.POST.get('content')))
				return render(request,'html/modifiquation.html',{'files':cloudfiles,'filecontent':request.POST.get('content'),'filename':request.POST.get("file"),'fileextention':request.POST.get("file").split('.')[-1],'menuliste':liste_menu})
		if request.POST.get('execut'):
			os.system('python3 static/default/cloud/'+str(request.POST.get('file')))
			return render(request,'html/modifiquation.html',{'files':cloudfiles,'filecontent':open('static/default/cloud/'+request.POST.get('file')).read(),'filename':request.POST.get("file"),'fileextention':request.POST.get("file").split('.')[-1],'menuliste':liste_menu})

#############
### CLOUD ###
#############

def cloud(request):

	if request.method == 'GET':
		return render(request,'html/multimedia.html',{'files':cloudfiles,'menuliste':liste_menu})
	if request.method == 'POST':
		if request.POST.get("delet") :
			os.system('cd static/default/cloud && rm -R '+request.POST.get("delet"))
			return render(request,'html/multimedia.html',{'files':cloudfiles,'menuliste':liste_menu})

def cloudapi(request):

	return render(request,'html/cloudapi.html',{'files':cloudfiles,'menuliste':liste_menu})

def cloud_envoyer_fichier(request):

	if request.GET.get('nom_fichier'):
		fichier_base_64 = fichier_vers_base64('static/default/cloud/' + request.GET.get('nom_fichier'))
		#print(fichier_base_64[:6].decode('utf-8'))
	return render(request,'html/multimedia.html',{'files':cloudfiles,'menuliste':liste_menu,'message_réussite':'Le fichier a bien été envoyé'})

def now(request):

	#print (liste_menu)
	if request.method == 'GET':
		return render(request,'html/now.html',{'menuliste':liste_menu})


def heure_vers_minute(monheure):
	return monheure * 60

@csrf_exempt
def reveil_web (request):

	if request.method == 'POST':
		if request.POST.get("heures_travail") and request.POST.get("minutes_travail") and request.POST.get("heure_preparation") and request.POST.get("minutes_preparation") and request.POST.get("heures_itineraire") and request.POST.get("minutes_itineraire") and request.POST.get("vitesse"):
			# Travail
			minutes_heures_travail      = int(heure_vers_minute(int(request.POST.get("heures_travail"))))
			minutes_travail             = int(request.POST.get("minutes_travail"))
			# Préparation
			minutes_heure_preparation   = int(heure_vers_minute(int(request.POST.get("heure_preparation"))))
			minutes_preparation         = int(request.POST.get("minutes_preparation"))
			# Itinéraire
			minutes_heures_itineraire   = int(heure_vers_minute(int(request.POST.get("heures_itineraire"))))
			minutes_itineraire          = int(request.POST.get("minutes_itineraire"))
			# Vitesse
			vitesse                     = int(request.POST.get("vitesse"))
			# Cycles
			temps_cycle = 6*90
			# Total
			reveil_time = minutes_heures_travail + minutes_travail - minutes_heure_preparation + minutes_preparation + minutes_heures_itineraire + minutes_itineraire + temps_cycle
			print (reveil_web)
			reveil_web_2 = float(reveil_web)/60
			print (reveil_web_2)

			reveil_web_message = "Votre reveil a bien été programé"

		else :
			reveil_web_message = "Tous les champs n'ont pas été rempli. Veillez corriger."
		return render(request,'html/reveil.html',{'message':reveil_web_message})
	else :
		return render(request,'html/reveil.html',{'menuliste':liste_menu})


def scenario(request):

	return render(request,'html/scenario.html',{'menuliste':liste_menu})

def home(request):

	return render(request, 'html/index.html', {'files':cloudfiles ,'menuliste':liste_menu})

def countnow(request):
	if request.method == 'GET':
		if request.GET.get("id") and request.GET.get("url"):
			update_menu(int(request.GET.get("id")))
			return render(request, 'html/countnow.html', {'url':str(request.GET.get("url"))})
		else :
			return render(request, 'html/error/400.html', {})
	return render(request, 'html/error/405.html', {'menuliste':liste_menu,'message':''})
			
def preferences(request):

	if request.GET.get('nom_user') :
		with open('datas/preferences.json', 'r+') as file:
			global preferences
			for i in request.GET :
				preferences[i]=str(request.GET.get(i))
				if 'mail' in i:
					preferences['mail'][i.split('mail')[1]] = request.GET.get(i)
			preferences_json = json.dumps(preferences,indent=4,ensure_ascii=False)
			file.seek(0)
			file.write(preferences_json)
			file.truncate()
	return render(request,'html/preferences.html',{'menuliste':liste_menu,'preferences':preferences})

def mamaison(request):

	if request.GET.get('maison'):
		pass
	return render(request, 'html/maison.html', {'menuliste':liste_menu,'pieces':pieces})

def qreaction(request) :
	toreturn = 'NO'
	if request.GET.get('action') :
		toreturn = 'ok'
		doaction(request.GET.get('action'))

	return HttpResponse(toreturn, content_type="text/plain")
def action(request):
	if request.GET.get('annee') and request.GET.get('mois') and request.GET.get('jours') and request.GET.get('heure') and request.GET.get('minute') and request.GET.get('action'):
		annee   = int(request.GET.get('annee'))
		mois    = int(request.GET.get('mois'))
		jours   = int(request.GET.get('jours'))
		heure   = int(request.GET.get('heure'))
		minute  = int(request.GET.get('minute'))
		action_ = request.GET.get('action')
		text = request.GET.get('text')
		id = 0
		for i in action :
			if i['id'] > 0 : id = i['id']
		id = id+1
		date = datetime(annee, mois, jours, heure, minute)
		cmd_list=["cd {dossier_script} && python3 manage.py action {id}".format(dossier_script=dossier_script,id=id)]
		job=atjob.Atjob()
		job.add(cmd_list)
		job_id=job.create(date,remove=False)
		action.append({'annee':annee,'mois':mois,'jours':jours,	'heure':heure,'minute':minute,'action':action_,'text':text,'terminal':'espeak \'{}\''.format(text),'job_id':job_id,'id':id,'temps':str(date)})
		variable_to_json(action,'datas/action.json')
		return render(request, 'html/action.html', {'files':cloudfiles ,'menuliste':liste_menu})
	else :
		return render(request ,'html/action.html', {'files':cloudfiles,'menuliste':liste_menu,'action':action})

def musique(request):
	if request.method == 'POST':
		return render(request ,'html/error/405.html', {'menuliste':liste_menu,'message_error':'Vous ne pouvez pas utiliser la mehode post !'})
	else :
		if "STOP" ==  musiqueetat()['state']   :
			os.system("mocp -S && mocp -c && mocp -a static/default/cloud")
		if request.GET.get("etat"):
			return HttpResponse(json.dumps(musiqueetat()),content_type="application/json")
		if request.GET.get('start'):
			os.system("mocp -p")
			return HttpResponse(json.dumps({'etat':musiqueetat(),'message':'La musique a été lancée'}),content_type="application/json")
								
		if request.GET.get('playpause'):
			os.system("mocp -G")
			return HttpResponse(json.dumps({'etat':musiqueetat(),'message':'La musique est en pause'}),content_type="application/json")
		elif request.GET.get('stop'):
			os.system("mocp -x")
			return HttpResponse(json.dumps({'etat':musiqueetat(),'message':'La musique est aretée'}),content_type="application/json")
		elif request.GET.get('suivant'):
			os.system("mocp -f")
			return HttpResponse(json.dumps({'etat':musiqueetat(),'message':'Le moreceau suivant est en lecture'},indent=4), content_type="application/json")
		elif request.GET.get('precedent'):
			os.system("mocp -r")
			return HttpResponse(json.dumps({'etat':musiqueetat(),'message':'Le moreceau précedent est en lecture'},indent=4), content_type="application/json")
		else :
			return render(request ,'html/musique.html', {'menuliste':liste_menu,'etat':musiqueetat()})
#####################
### FIN PAGES WEB ###
#####################
