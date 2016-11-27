import os
from threading import Thread

class downloader(Thread):
	def __init__(self,file_url):
		Thread.__init__(self)
		self.file_url = file_url
	def download(self,url):
		
		if '://youtube.' in self.file_url or '://www.youtube.' in url  :
			os.system('cd static/cloud/ && youtube-dl'+ url)
		else :
			os.system('cd static/cloud/ && wget '+url)
		
		
	def run (self):
		for i in self.file_url.split(' ') :
			print ('Download Start With URL :'+ i)
			self.download(i)
			print ('Download Stop')
		
		


"""
Exemple d'utilisation:

dwn1 = downloader('http://herveprojet.hol.es')
dwn1.run()

"""
