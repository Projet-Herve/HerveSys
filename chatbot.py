import re
import json
import random
import requests
from myhtml import tag
from datas import *


class Reponse():

    """docstring for reponse"""

    def __init__(self, arg={}):
        self.text = arg.get("text", "")
        self.links = arg.get("links", "")
        self.html = arg.get("html", "")
        self.datas = arg.get("datas", "")

    def get_text(self):
        return self.text

    def get_links(self):
        return self.links

    def get_html(self):
        return self.html

    def get_datas(self):
        return self.datas

    def get_all(self):
        return locals()


class question ():

    def __init__(self, message, **kwargs):
        self.message = [message, message.lower(), message.lower()]
        self.final = {"reponses": [], "regexs": [], "nbcorrection": 0}
        self.user = None
        self.listdephrases = []
        self.plugins = []
        self.settings_file = "datas/settings.json"
        self.__dict__.update(kwargs)

    def load_user(self, user):
        users = load_datas(self.settings_file)
        if user != "":
            try:
                self.user = users[user]
            except:
                pass  # A finir
                self.user["profile"]["e"] = "e" if self.user[
                    "profile"]["sexe"] == "f" else ""
            return self.user
        # except:
        #    self.user = users['Demo']

    def load_plugins(self, plugins):
        for plugin in plugins:
            with open("apps/chatbot/" + plugin.split(".")[0] + ".py") as plugin_src:
                src = plugin_src.read()
                exec(src, {'q': self})
        return True

    def load_history(self, history):
        self.history = history

    def checkortho(self):
        nbcoorection = 0
        while nbcoorection < 25:
            tocorect = self.message[2]
            try:
                requette = requests.get(
                    "http://herveprojet.hol.es/web-app/api/ortho.php",
                    params={'text': tocorect}
                ).text
                correct = json.loads(requette)["AutoCorrectedText"].lower()
            except:
                print("can't correct")
                correct = tocorect
            if tocorect == correct:
                break
            else:
                self.message[2] = correct
                nbcoorection += 1
        self.final["nbcorrection"] = nbcoorection
        return self.message[2]

    def getreponse(self, reponse):
        if type(reponse) == str:
            try:
                return reponse.format(**self.user["profile"])
            except:
                return reponse
        elif type(reponse) == dict:
            return (self.getreponse(reponse[self.user["profile"]["phrase"]]))
        elif type(reponse) == list:
            try:
                return (random.choice(reponse).format(**self.user))
            except:
                return random.choice(reponse.get_text())

    def script(self, regexs):
        def decorator(function):
            self.listdephrases.append(regexs)
            for regex in regexs:
                if re.search(regex, self.message[2]):
                    reponse = function(re.search(regex, self.message[2]))
                    self.final["reponses"].append(Reponse(reponse))
                    self.final["regexs"].append(regex)
                    return reponse
        return decorator

    def liste_phrases(self):
        return self.listdephrases

    def reponse(self):
        return list(
            map(
                lambda reponse: self.getreponse(reponse.get_text()),
                self.final["reponses"]
            ))
        # return self.final["reponses"]

    def json(self):
        the_l = self.reponse()
        toreturn = {
            "text": {
                "initial": self.message[0],
                "lower": self.message[1],
                "corrected": self.message[2]
            },
            "reponses": {
                "text": " ".join(the_l),
                "html": "".join(
                        list(
                            map(
                                lambda x: self.getreponse(x.get_html()).format(
                                    **self.user["profile"]),
                                self.final["reponses"]
                            )
                        )
                ),
                "links": [],
                "list": the_l
            },
            "regexs": self.final["regexs"],
            "nbcorrection": self.final["nbcorrection"]
        }
        for res_ in self.final["reponses"]:
            toreturn["reponses"]["links"].extend(res_.get_links())

        # toreturn["regexs"] = self.final["regexs"]
        toreturn = json.dumps(toreturn, sort_keys=True, indent=4)
        return toreturn
