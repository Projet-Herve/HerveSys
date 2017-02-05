@myapp.in_thread
def arduino_():
    ser = False
    delais = 10
    while True:
        if ser:
            myapp.arduino = True
            arduinojson = ser.readline()
            arduinojson = json.loads(arduinojson)
            if arduinojson["value"] < 500:
                pass  # print("il y a peut de lumière !")
            # print(arduinojson["level"])
        else:
            sleep(delais)
            myapp.arduino = False
            ser = arduino.connect(error=False)
            delais = delais + 10
