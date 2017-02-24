import json

messages = json.loads(open("train.json", "r").read())


class analizer():

    def __init__(self, messages):
        self.messages = messages
        self.mi = json.loads(open("words.json", "r").read())

    def responses(self, for_):
        responses = list()
        finale = list()
        finale_2 = dict()
        interv_suivant = None
        for message in self.messages:
            if set(for_.lower().split(" ")).issubset(message["text"].lower().split(" ")):
                for r in self.messages[self.messages.index(message)+1:]:
                    if r["from"] == message["from"]:
                        responses.extend(
                            self.messages[
                                self.messages.index(message)+1:self.messages.index(r)]
                        )
                        interv_suivant = r["text"]
                        break
                    if self.messages[self.messages.index(r)] == self.messages[-1]:
                        responses.extend(
                            self.messages[self.messages.index(message):]
                        )
                        break

        for i in responses:
            text = i["text"]
            text = text.split(" ")
            for w in text:
                if w in self.mi:
                    text.remove(w)
            finale.extend(text)

        for i in finale:
            if not finale_2.get(i):
                finale_2[i] = finale.count(i)

        return finale_2, interv_suivant


a = analizer(messages)
print(a.responses(input(">")))
