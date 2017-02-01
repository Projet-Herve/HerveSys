import json

def load_datas(file):
    file = open("datas/" + ".".join(file.split(".")[:-1]) + ".json").read()
    return json.loads(file)


def update_datas(var, file):
    with open("datas/" + file.split(".")[0] + ".json", "w") as filedata:
        # .encode('utf8'))
        filedata.write(json.dumps(var, indent=4, ensure_ascii=False))
