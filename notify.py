from pushbullet import Pushbullet
import datas


def send_pushbullet_note(users, title, body):
    for user in users:
        if datas.load_datas("settings")[user].get("pushbullet"):
            try:
                pb = Pushbullet(datas.load_datas("settings")[
                                user]["pushbullet"]["api_key"])
                return pb.push_note("{title} - Hervé".format(title=title), body)
            except Exception as e:
                print("[erreur] " + e)
        else:
            print("[erreur] Impossible d'envoyer une notification push à " +
                  user + " car il ne possede pas de préférences pour pushbullet")
