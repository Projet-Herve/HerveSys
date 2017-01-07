import json
import serial
import time


class ConnectionError(Exception):
    pass


def connect(locations=[
    '/dev/ttyUSB0',
    '/dev/ttyUSB1',
    '/dev/ttyUSB2',
    '/dev/ttyUSB3',
    '/dev/ttyS0',
    '/dev/ttyS1',
    '/dev/ttyS2',
    '/dev/ttyS3',
    '/dev/ttyACM0',
    '/dev/ttyACM1',
    '/dev/ttyACM2',
        '/dev/ttyACM3'], port=9600):
    print('Test de connexion')
    ser = False
    for device in locations:
        try:
            ser = serial.Serial(device, port)
            time.sleep(5)
            ser.write('hello arduino'.encode())
            ser.readline()
            print("Arduino connecter a :", device)
            return ser
        except:
            #print ("Impossible de se connecter a :",device)
            pass
    if ser == False:
        raise ConnectionError("Aucune connexion n'a pu être établie...")


def output(pin, connexion):
    if connexion != False:
        mystr = 'pin ' + str(pin) + ' output'
        connexion.write(mystr.encode())
    else:
        raise ConnectionError("Aucune connexion n'existe")


def on(pin, connexion):
    if connexion != False:
        mystr = 'pin ' + str(pin) + ' on'
        connexion.write(mystr.encode())
    else:
        raise ConnectionError("Aucune connexion n'existe")


def off(pin, connexion):
    if connexion != False:
        mystr = 'pin ' + str(pin) + ' off'
        connexion.write(mystr.encode())
    else:
        raise ConnectionError("Aucune connexion n'existe")


def blink(pin, connexion):
    if connexion != False:
        mystr = 'pin ' + str(pin) + ' blink'
        connexion.write(mystr.encode())
    else:
        raise ConnectionError("Aucune connexion n'existe")


def fade(pin, connexion):
    if connexion != False:
        mystr = 'pin ' + str(pin) + ' fade'
        connexion.write(mystr.encode())
    else:
        raise ConnectionError("Aucune connexion n'existe")


def read(connexion):
    if connexion != False:
        return str(connexion.readline())
    else:
        raise ConnectionError("Aucune connexion n'existe")


def write(text, connexion):
    if connexion != False:
        connexion.write(text.encode())
    else:
        raise ConnectionError("Aucune connexion n'existe")


def deconnect(connexion):
    if connexion != False:
        connexion.close()
    else:
        raise ConnectionError("Aucune connexion n'existe")
