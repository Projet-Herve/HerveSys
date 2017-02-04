import json

def load_datas(file):
    file = open(file).read()
    return json.loads(file)


def update_datas(var, file):
	open(file, "w").write(json.dumps(var, indent=4, ensure_ascii=False))
