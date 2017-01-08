import json
from datetime import date, time, datetime


class agenda():

    def __init__(self, file="agenda.json"):
        self.file = file
        self.agenda = json.loads(open('datas/' + self.file, "r").read())

    def __write_agenda(self):
        with open("datas/" + self.file, "w") as file:
            try:
                file.write(json.dumps(self.agenda, indent=4))
                return True
            except Exception as e:
                print(e)
                return False

    def datetime_to_dict(self, evenement):
        return {"year": evenement.year, "month": evenement.month, "day": evenement.day, "hour": evenement.hour, "minute": evenement.minute}

    def nouveau_evenement(self, evenement):
        id = len(self.agenda) + 1
        self.agenda[id] = evenement
        return (self.__write_agenda())

    def modifier_evenement(self, id, evenement):
        try:
            self.agenda[id] = evenement
            return (self.__write_agenda())
        except Exception as e:
            raise 'L\'evenement n\'exitse pas'


# myagenda = agenda()
# evenement = myagenda.datetime_to_dict(datetime.now())
# evenement["day"] += 2
# evenement["month"] += -1
# print(evenement)
# result = myagenda.nouveau_evenement(evenement)
