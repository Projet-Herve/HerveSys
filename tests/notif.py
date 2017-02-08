def createnotif():
    for user in myapp.users:
        if "notif" in myapp.users[user]:
            myapp.notif([user],"Salut","je t'envoie une notif :)", pushbullet_notif= False)
        else:
            myapp.users[user]["notif"] = list()
    return True
    
schedule.every(10).seconds.do(createnotif)
