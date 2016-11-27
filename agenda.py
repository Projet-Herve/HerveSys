import json


class agenda():
	def __init__ (self,file="agenda.json"):
		self.file = file
		self.agenda = json.loads(open('datas/'+file,"r").read())

	def __write_agenda(self):
		with open("datas/"+file,"w") as file:
			try:
				file.write(json.dumps(self.agenda,indent=4))
				return True
			except Exception as e:
				return False

	def nouveau_evenement(self,evenement):
		id = int(len(self.agenda)) + 1
		self.agenda[id] = evenement
		return (self.__write_agenda(),id)

	def modifier_evenement(self,id,evenement):
		try:
			self.agenda[id] = evenement
			return (write_file(),self.agenda[id])
		except Exception as e:
			raise 'L\'evenement n\'exitse pas'


"""
newagenda = 'agenda.json'
result = nouveau_evenement(newagenda,{'jour':'z','mois':'gz','annee':'zs','heure':'hz','minute':'zs'})
modifier_evenement(newagenda,result[1],{'jour':'zddddd','mois':'gz','annee':'zs','heure':'hmmmz','minute':'zs'})
"""