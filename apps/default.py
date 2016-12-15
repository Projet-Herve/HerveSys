from io import StringIO
import requests

@q.script(["herve"])
def me(regex):
	return {"text":"oui {civilite} ?"}



@q.script([r"cucu",r"bonjour",r"plop",r"salut",r"slt",r"hey",r"hello",r"yop","yo"])
def salutation(regex):
	return {"text":{'soutenu' :['bonjour {civilite}','mes salutations {civilite}'],'courant' : ["plop","salut","slt","hey","hello","yop",]}}

@q.script([r"mets( la (télé|tele|télévision))? sur la (?P<chaine>.*)"])
def changechain(regex):
	import fbxremote
	remote = fbxremote.remote(66412704)
	print(remote.buttons(regex.group("chaine")))
	return {"text":reponse({"text":"J'ai changé de chaine"})}

@q.script([r"comment (?P<recherche>(\w|\s)+)"])
def how(regex):
	toreturn = StringIO()
	if regex.group("recherche") == "vas":
		return {"text":["je vais bien {civilite}"]}
	else :
		group = "comment " + regex.group('recherche')
		requette = requests.get('https://searx.me', params = {'format':'json','q':group}).text
		try :
			myjson = json.loads(requette)
			reponse = myjson["results"]
			print ("Voila le meilleur résultat que j'ai pu trouver :",file=toreturn)
			print ("\n\t" + reponse[0]["title"] + "\n\t" + reponse[0]["url"],file=toreturn)
			print("\nJ'ai aussi trouvé :",file=toreturn)
			for i in range(4):
				i +=1
				print ("\n\t" + reponse[i]["title"] + "\n\t" + reponse[i]["url"],file=toreturn)
		except :
			print('excusé(e) moi {civilite}, je n\'est rien pu trouver',file=toreturn)
		return {"text":toreturn.getvalue()}


@q.script([r"commençons à nous connaître"])
def learnaboutuser(regex):
	return {"text":"tres bien"}

@q.script([r"qui est (?P<personne>(\w|\s)+)"])
def whois(regex):
	if regex.group('personne'):
		recherche = regex.group('personne')
		requette = requests.get('https://searx.me', params = {'format':'json','q':recherche}).text
		if regex.group('personne') == "jules michael":
			reponse= "Mon créateur"
		elif requette == "Rate limit exceeded" :
			reponse =  "Impossible de vous dire qui est " + regex.group('personne') + " car searx.me n'authorise plus de requette"
		else :
			myjson = json.loads(requette)
			reponse = "D'apres wikipedia :"+  str(myjson["results"][0]["content"])
		return {"text":reponse}


@q.script([r"je t'aime"])
def jtm(regex):
	return {"text":"mais enfin {civilite} ce n'est pas possible"}

@q.script([r"lis moi (cet article |cette page )?(?P<url>(.)*)"])
def lecteurarticle(regex):
	import articleextractor
	if regex.group("url"):
		article = articleextractor.extract(regex.group("url"))
		return({"text":"Voila votre article:\n"+article})

@q.script([r"que puis(\-)?( )?je te dire( \?)?"])
def listphrases(regex):
	toreturn = StringIO()
	print ("Vous pouvez me dire :",file=toreturn)
	thislist = q.listphrases()
	for i in thislist :
		print ( "\t- " + str(i),file=toreturn)
	return {"text":toreturn.getvalue()}