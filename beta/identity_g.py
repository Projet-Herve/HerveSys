import random


def phone():
    # liste = random.shuffle([i for i in range(10)])
    liste = [str(random.randint(10,99)) for i in range(5)]
    phone_n = " ".join(liste)
    return phone_n


for i in range(10):
    print(phone())
