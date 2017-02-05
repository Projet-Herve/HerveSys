import requests


class remote():

    """docstring for remote"""

    def __init__(self, code, box=1):
        self.box = box
        self.code = code

    def request(self, button, long=False):
        box = "hd" + str(self.box)

        if long == False:
            long = "false"
        else:
            long = "true"

        params = {
            "code": self.code,
            "key": button,
            "long": long,
        }

        result = requests.get(
            url="http://{box}.freebox.fr/pub/remote_control/".format(box=box),
            params=params
        )

        return result

    def buttons(self, buttons, long=False):
        results = []
        for button in buttons:
            result = self.request(button, long=long)
            results.append(result)
        return results

"""

"red" // Bouton rouge
"green" // Bouton vert
"blue" // Bouton bleu
"yellow" // Bouton jaune


"power" // Bouton Power
"list" // Affichage de la liste des chaines
"tv" // Bouton tv

"0" // Bouton 0
"1" // Bouton 1
"2" // Bouton 2
"3" // Bouton 3
"4" // Bouton 4
"5" // Bouton 5
"6" // Bouton 6
"7" // Bouton 7
"8" // Bouton 8
"9" // Bouton 9

"back" // Bouton jaune (retour)

"swap" // Bouton swap

"info" // Bouton info
"epg" // Bouton epg (fct+)
"mail" // Bouton mail
"media" // Bouton media (fct+)
"help" // Bouton help
"options" // Bouton options (fct+)
"pip" // Bouton pip

"vol_inc" // Bouton volume +
"vol_dec" // Bouton volume -

"ok" // Bouton ok
"up" // Bouton haut
"right" // Bouton droite
"down" // Bouton bas
"left" // Bouton gauche

"prgm_inc" //Bouton programme +
"prgm_dec" // Bouton programme -

"mute" // Bouton sourdine
"home" // Bouton Free
"rec" // Bouton Rec

"bwd" // Bouton << retour arrière
"prev" // Bouton |<< précédent
"play" // Bouton Lecture / Pause
"fwd" // Bouton >> avance rapide
"next" // Bouton >>| suivant

"""
