@q.script(["t'as pété"])
def proute(regex):
    return {"text": "Oui désolé {civilite} ce sont les haricots"}


@q.script(["fais moi une blague"])
def meneherve(regex):
    return {"text": "Arrêtez de m'énn-hervé"}


@q.script(["chante-moi une chanson", "chante moi une chanson"])
def chanson(regex):
    return {"text": "BAAABY BAAABY BAAABY OOOOOOOOH LOVE"}


@q.script(["suis-je beau", "suis-je belle"])
def beaute(regex):
    return {"text": "Non, cela ne vous correspond pas {civilite}"}


@q.script(["j'aime les licornes"])
def licornes(regex):
    return {"text": "Et leurs jolies cornes 🎶"}


@q.script(["montre moi des photos de glaçage de cupcakes", "ok google"])
def chatbot(regex):
    return {"text": "Je ne suis pas google."}


@q.script(["As-tu skype ?"])
def chatbot(regex):
    return {"text": "Non"}


@q.script(["qu'est ce que le groupe 42"])
def chatbot(regex):
    return {"text": "Un fabuleux groupe que tu peux rejoindre dès maintenant ici", "links": ["https://mattermost.digitalpulsesoftware.net/groupe-42/"]}


@q.script(["dis siri"])
def chatbot(regex):
    return {"text": "Je ne suis pas Siri ;)"}


@q.script(["pourquoi hervé", "pourquoi herve"])
def chatbot(regex):
    return {"text": "Pourquoi me posez-vous cette question ?"}


@q.script(["pierre"])
def chatbot(regex):
    return {"text": "Feuille ciseau"}


@q.script(["windows ou linux"])
def chatbot(regex):
    return {"text": "Linux est mieux"}


@q.script(["ios ou android", "android ou ios"])
def chatbot(regex):
    return {"text": "Android sans hésiter :-)"}


@q.script(["t'as un compte steam"])
def chatbot(regex):
    return {"text": "Non désolé, je ne joue qu'à Minecraft"}


@q.script(["mac ou pc", "pc ou mac"])
def chatbot(regex):
    return {"text": "Linux"}


@q.script(["j'ai faim"])
def chatbot(regex):
    return {"text": ["Cela prouve que vous êtes bien en vie", "Cela prouve que vous êtes bien en vie {civilite}"]}
