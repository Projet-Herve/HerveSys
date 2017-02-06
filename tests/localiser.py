@webapp.route('/localiser2')
@login_required
def localiser2():
    # MaxMind, GeoIP, minFraud, and related trademarks are the trademarks of
    # MaxMind, Inc.
    message = {"error": [], "message": []}
    ip = request.args.get("ip")
    rawdata = pygeoip.GeoIP('datas/GeoLiteCity.dat')
    dataclient = rawdata.record_by_name(ip)
    dataserver = rawdata.record_by_name(
        load_datas(myapp.settings_file)["sys"]["house_ip"])
    cordoneesclient = (dataclient["longitude"], dataclient["latitude"])
    cordoneesserver = (dataserver["longitude"], dataserver["latitude"])
    d = vincenty(cordoneesclient, cordoneesserver).meters
    if d > 5 * 1000:
        print("Vous êtes loins de votre maison ! ({km} km)".format(km=d/1000))
    elif d == 0:
        print("Vous êtes chez vous.")
    else:
        print("Vous êtes proche de chez vous.")
    if dataclient:
        message["result"] = dataclient
    else:
        message["error"].append("Aucune IP n'a été renseignée")
    return(Response(response=json.dumps(message), status=200, mimetype="application/json"))
