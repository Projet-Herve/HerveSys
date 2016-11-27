import requests
from bs4 import BeautifulSoup
import json

def extract(url):
	file = open("datas/website.json","r").read()
	i = None
	for i in json.loads(file):
		if i["url"] in url :website = i;break
	page = requests.get(url).text
	soup = BeautifulSoup(page, 'html.parser')


	if i :
		if len(i["contenthead"]) == 1 :
			htmltext = (soup.find_all(i["contenthead"][0]))
		else:
			htmltext = (soup.find_all(i["contenthead"][0], class_=i["contenthead"][1]))
	else :
		htmltext = (soup.find_all("article"))
		
	print (htmltext)
	text =  " ".join(list(map(lambda p: p.get_text(), htmltext)))
	return text