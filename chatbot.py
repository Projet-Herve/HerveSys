import re
import json
import random
import requests


class Reponse():
	"""docstring for reponse"""
	def __init__(self, arg={}):
		self.text = arg.get("text",None)
		self.link = arg.get("link",None)
		self.html = arg.get("html",None)
		self.datas = arg.get("datas",None) 
	def get_text(self):
		return self.text
	def get_link(self):
		return self.link
	def get_html(self):
		return self.html
	def get_datas(self):
		return self.datas
	def get_all(self):
		return locals()

class question ():
	def __init__(self, message):
		self.message = [message,message.lower(),message.lower()]
		self.final = {"reponses":[],"regexs":[],"nbcoorection":0}
		self.user = None
		self.listdephrases = []
		self.plugins = []

	def load_user(self,user="default"):
		with open("datas/users.json", "r") as users:
			try:
				self.user = json.load(users)[user]
			except:
				self.user = json.load(users)['default']
			return self.user
      
	def load_plugins(self,plugins):
		for plugin in plugins:
			with open("app/"+plugin.split(".")[0]+".py") as plugin_src:
				src = plugin_src.read()
				exec(src, {'q': self})
		return True

	def checkortho(self):
		nbcoorection = 0
		while nbcoorection < 25:
			tocorect = self.message[2]
			try :
				requette = requests.get("http://herveprojet.hol.es/web-app/api/ortho.php",params={'text':tocorect}).text
				correct = json.loads(requette)["AutoCorrectedText"].lower()
			except:
				correct = tocorect
			if tocorect == correct :
				break
			else :
				self.message[2] = correct
				nbcoorection += 1
		self.final["nbcoorection"] = nbcoorection
		return self.message[2]

	def getreponse(self,reponse) :
		if type(reponse) == str :
			try :
				return reponse.format(**self.user) 
			except: return reponse
		elif type(reponse) == dict:	
			return (self.getreponse(reponse[self.user["phrase"]]))
		elif type(reponse) == list:
			try :
				return (random.choice(reponse).format(**self.user))
			except : return random.choice(reponse.get_text())
	
		
	def script (self,regexs):
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

	def reponse (self):
		return list(map(lambda reponse: self.getreponse(reponse.get_text()),self.final["reponses"]))
		# return self.final["reponses"]

	def json(self):
		toreturn = {
			"text": {
				"initial":self.message[0],
				"lower":self.message[1],
				"corrected":self.message[2]
			},
			"reponses":{
				"text": ". ".join(list(map(lambda x: self.getreponse(x.get_text()),self.final["reponses"]))),
				"list" : list(map(lambda x: self.getreponse(x.get_text()),self.final["reponses"]))
			},
			"regexs" : self.final["regexs"],
			"nbcoorection" : self.final["nbcoorection"]
		}
		#toreturn["regexs"] = self.final["regexs"]
		toreturn = json.dumps(toreturn, sort_keys=True, indent=4)
		return toreturn


