import chatbot
q = chatbot.question("Bonjour")
q.load_user()
q.load_plugins(["default"])
print(q.json())