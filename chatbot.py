import re
import json
import random

class question ():
	def __init__(self, message):
		self.message = [message,message.lower(),message.lower()]
		self.final = {"reponses":[],"regexs":[],"nbcoorection":0}
		self.user = None
		self.listdephrases = []
		self.plugins = []

	def load_user(self,thisfile):
		with open(thisfile, "r") as user:
			self.user = json.loads(user.read())
			return self.user

	def load_plugins(self,plugins):
		for plugin in plugins:
			with open("plugins/chatbot/"+plugin.split(".")[0]+".py") as plugin_src:
				src = plugin_src.read()
				exec(src, {'q': self})

	def checkortho(self):
		import requests
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
		if not self.user :
			self.load_user("datas/default.json")

		if type(reponse) == str :
			try :
				return reponse.format(**self.user) 
			except: return reponse
		elif type(reponse) == dict:	
			return (self.getreponse(reponse[self.user["phrase"]]))
		elif type(reponse) == list:
			try :
				return (random.choice(reponse).format(**self.user))
			except : return random.choice(reponse)
		else:
			raise "WTF"
		
	def script (self,regexs):
		def decorator(function):
			self.listdephrases.append(regexs)
			for regex in regexs:
				if re.search(regex, self.message[2]):
					reponse = function(re.search(regex, self.message[2]))
					self.final["reponses"].append(self.getreponse(reponse))
					self.final["regexs"].append(regex)
					return reponse
		return decorator

	def liste_phrases(self):
		return self.listdephrases

	def reponse (self):
		return (". ".join(self.final["reponses"]))

	def json(self):
		toreturn = {
			"text": {
				"initial":self.message[0],
				"lower":self.message[1],
				"corrected":self.message[2]
			},
			"reponses":{
				"text": ". ".join(self.final["reponses"]),
				"list" : self.final["reponses"]
			},
			"regexs" : self.final["regexs"],
			"nbcoorection" : self.final["nbcoorection"]
		}
		#toreturn["regexs"] = self.final["regexs"]
		toreturn = json.dumps(toreturn, sort_keys=True, indent=4)
		return toreturn



class reponse():
	"""docstring for reponse"""
	def __init__(self, arg):
		self.text = []
		self.link = None
		self.html = None
		self.datas = None


"""
Une reponse retrournee par une fonction vas etre defini par :
	r = hcb.reponce()
	r.text("voila une video de chat")
	r.html("<iframe width="560" height="315" src="https://www.youtube.com/embed/cggl4WN77Mw" frameborder="0" allowfullscreen></iframe>")
	r.datas({"type":"video","url":"https://www.youtube.com/embed/cggl4WN77Mw", "service":"youtube"})
"""
	
