from Exode import *
s =BOARD.search()
print(s)
uno = Board(s[0])
analog= AnaPin(1,'INPUT')
analog.read()
def printValue(pin):
  print(str(pin._pin)+": "+str(pin.value))
analog.attachEvent("update",printValue)
analog.listen()
print(analog.value)
