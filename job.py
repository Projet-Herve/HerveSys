import requests

def theme_update(setings):
    try :
        requests.get(setings["theme"][setings["theme"]["actual"]]["safeurl"]).text
        
        for file in setings["theme"][setings["theme"]["actual"]]["css"]:
            container = requests.get(file["url"])
            
        for file in setings["theme"][setings["theme"]["actual"]]["js"]:
            container = requests.get(file["url"])    
    except: pass