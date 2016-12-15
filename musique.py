import subprocess
def musiqueetat():
	etat = subprocess.Popen(['mocp','-Q','%state:/%file:/%title:/%artist:/%song:/%album:/%tt:/%tl:/%ts:/%ct:/%cs:/%b:/%r'], stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split(':/')
	finaletat = {}
	
	"""
	data_keys = ['state', 'file', 'title', 'artist', 'album', 'song', ...]
    ["state" ,"file" ,"title" ,"artist" ,"song" ,"album" ,"tt" ,"tl" ,"ts" ,"ct" ,"cs" ,"b" ,"r"]
	mocp_args = '%' + ':/%'.join(data_keys)
	data_values = subprocess.Popen(['mocp', '-Q', args], stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split(':/')
	data = zip(data_keys, data_values)
	"""


	if 'FATAL_ERROR' in etat[0] or '' == etat[0]:
		finaletat['state'] = 'STOP'
	else :
		finaletat['state']=  etat[0]
		finaletat['file']=   etat[1]
		finaletat['title']=  etat[2]
		finaletat['artist']= etat[3]
		finaletat['song']=   etat[4]
		finaletat['album']=  etat[5]
		finaletat['tt']=     etat[6]
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


"""
def musique(request):
	if request.method == 'POST':
		return render(request ,'html/error/405.html', {'menuliste':liste_menu,'message_error':'Vous ne pouvez pas utiliser la method post !'})
	else :
		if "STOP" ==  musiqueetat()['state']   :
			os.system("mocp -S && mocp -c && mocp -a static/cloud")
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
			return HttpResponse(json.dumps({'etat':musiqueetat(),'message':'Le morceau suivant est en lecture'},indent=4), content_type="application/json")
		elif request.GET.get('precedent'):
			os.system("mocp -r")
			return HttpResponse(json.dumps({'etat':musiqueetat(),'message':'Le morceau précedent est en lecture'},indent=4), content_type="application/json")
		else :
			return render(request ,'html/musique.html', {'menuliste':liste_menu,'etat':musiqueetat()})
"""