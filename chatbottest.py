import chatbot
q = chatbot.question("bonjour comment vas tu ?")
q.load_user()
q.load_plugins(["default"])
print(q.json())