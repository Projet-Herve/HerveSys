from pushbullet import Pushbullet
import datas



def send_pushbullet_note(user,title,body):
    pb = Pushbullet(datas.load_datas("settings")[user]["pushbullet"]["api_key"])
    return pb.push_note("{title} - From Hervé".format(title=title),body)
