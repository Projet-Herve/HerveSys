from pushbullet import Pushbullet
import datas

pb = Pushbullet(datas.load_datas("setings")["pushbullet"]["api_key"])

def send_pushbullet_note(title,body):
	return pb.push_note("{title} - From Hervé",body)

def pushbullet():
	return Pushbullet