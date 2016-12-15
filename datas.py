import json

def load_datas(file):
    file = open("datas/"+file.split(".")[0]+".json").read()
    return json.loads(file)

def update_datas(var,file):
	with open("datas/"+file,"w") as filedata:
		filedata.write(json.dumps(var,indent=4,ensure_ascii=False))#.encode('utf8'))