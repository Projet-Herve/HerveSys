from io import StringIO
import requests
import json


@q.script(["herve"])
def me(regex):
    return {"text": "oui {civilite} ?"}


@q.script([r"cucu", r"bonjour", r"plop", r"salut", r"slt", r"hey", r"hello", r"yop", "yo", r"coucou", r"wsh", "wesh"])
def salutation(regex):
    return {"text": {'soutenu': ['bonjour {civilite}', 'mes salutations {civilite}'], 'courant': ["plop", "salut", "slt", "hey", "hello", "yop", ]}}


@q.script([r"mets( la (télé|tele|télévision))? sur la (?P<chaine>.*)"])
def changechain(regex):
    import fbxremote
    remote = fbxremote.remote(66412704)
    print(remote.buttons(regex.group("chaine")))
    return {"text": "J'ai changé de chaine"}


@q.script([r"comment (?P<recherche>(\w|\s)+)"])
def how(regex):
    toreturn = ""
    html = ""
    if regex.group("recherche") == "vas tu" or regex.group("recherche") == "vas-tu":
        return {"text": ["Je vais bien {civilite}"]}
    else:
        pass
        # group = "comment " + regex.group('recherche')
        # requette = requests.get('http://api.duckduckgo.com/', params = {'format':'json','q':group}).text
        # try :
        #   myjson = json.loads(requette)
        #   reponse = myjson["results"]
        #   toreturn += "Voila le meilleur résultat que j'ai pu trouver :"
        #   toreturn += "\n\t" + reponse[0]["title"] + "\n\t" + reponse[0]["url"]
        #   toreturn += "\nJ'ai aussi trouvé :"
        #   for i in range(4):
        #       i +=1
        #       html += tag("a",href=reponse[i]["url"],contenu=reponse[i]["title"])
        #       toreturn += ("\n\t" + reponse[i]["title"] + "\n\t" + reponse[i]["url"])
        # except Exception as e  :
        #   toreturn = 'Excusé{e} moi {civilite}, je n\'est rien pu trouver'
        #   print (e,requette)
        return {"text": toreturn, "html": html}


@q.script([r"commençons à nous connaître"])
def learnaboutuser(regex):
    return {"text": "tres bien"}


@q.script([r"qui est (?P<personne>.*)"])
def whois(regex):
    if regex.group('personne'):
        recherche = regex.group('personne')
        requette = requests.get(
            'https://searx.me', params={'format': 'json', 'q': recherche}).text
        if regex.group('personne') == "jules michael" or "jules michael" in regex.group('personne'):
            reponse = "Mon créateur !! C'est un formidable personnage ^^. Voila un lien qui pourra vous aider ;)"
            links = ["https://github.com/JulesMichael"]
        elif requette == u"Rate limit exceeded":
            reponse = "Impossible de vous dire qui est " + \
                regex.group('personne') + \
                " car searx.me n'authorise plus de requette"
        else:
            myjson = json.loads(requette)
            reponse = "D'apres wikipedia :" + \
                str(myjson["results"][0]["content"])
        return {"text": reponse, "links": links}


@q.script([r"je t'aime"])
def jtm(regex):
    return {"text": "mais enfin {civilite} ce n'est pas possible"}


@q.script([r"ca va"])
def chatbot(regex):
    return {"text": "oui {civilite}"}


@q.script([r"lis moi (cet article |cette page )?(?P<url>(.)*)"])
def lecteurarticle(regex):
    import articleextractor
    if regex.group("url"):
        article = articleextractor.extract(regex.group("url"))
        return({"text": "Voila votre article:\n" + article})


@q.script([r"que puis(\-)?( )?je te dire( \?)?"])
def listphrases(regex):
    toreturn = "Vous pouvez me dire :"
    thislist = q.listphrases()
    for i in thislist:
        toreturn += "\t- " + str(i)
    return {"text": toreturn}
