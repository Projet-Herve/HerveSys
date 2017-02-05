def createnotif():
    print("NOTIF")
    for user in myapp.users:
        if "notif" in myapp.users[user]:
            myapp.users[user]["notif"].append("Hey !")
        else:
            myapp.users[user]["notif"] = list()
    return True
schedule.every().seconds.do(createnotif)