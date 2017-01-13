$.get("http://ipinfo.io", function(response) {
    ip = response.ip;
    log>ip;
    $.get("/localiser", {ip:ip}, function(selfresponse){
        log>"Votre localisation:";
        log>selfresponse;
    });
}, "jsonp");