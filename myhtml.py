
def tag(tag, **kwargs):
    html = "<" + tag
    for attribut in kwargs:
        if attribut != "contenu":
            if attribut[-1] != "_":
                html += " " + attribut + "=\"" + \
                    " ".join(
                        list(map(lambda value: str(value), kwargs.get(attribut)))) + "\""
            else:
                html += " " + attribut[:-1] + "=\"" + " ".join(
                    list(map(lambda value: str(value), kwargs.get(attribut)))) + "\""

    if kwargs.get("contenu"):
        html += ">\n" + "\t" + kwargs.get("contenu")
        html += "</" + tag + ">\n"
    else:
        html += "/>\n"
    return html
