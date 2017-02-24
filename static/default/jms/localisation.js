$.get("http://ipinfo.io", function(response) {
    ip = response.ip;
    $.get("/localiser", {ip:ip}, function(selfresponse){
        //log>"Votre localisation:";
        log>selfresponse;
         var map = L.map('map').setView([selfresponse.result.latitude, selfresponse.result.longitude], 10);
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        L.marker([selfresponse.result.latitude, selfresponse.result.longitude]).addTo(map)
            .bindPopup(`${selfresponse.result.city} ${selfresponse.result.postal_code}, ${selfresponse.result.country_name}`)
    });
}, "jsonp");