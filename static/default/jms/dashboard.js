function ù() {
    $(".item").first().addClass("select")
    log>$(".item").first();
}

Mousetrap.bind('right', function(e) {
    $(".select").removeClass("select").next().addClass("select");
})

Mousetrap.bind('left', function(e) {
    $(".select").removeClass("select").prev().addClass("select");
})


$(document).ready(function() {
    if(user != "") {
        $('.text-green').hide().html('<div class="container">\
                    <center>\
                    <div id="hello">\
                        <p class="text" style="font-size: 50px;">\
                            Bonjour ' + user.profile.nom + ' !\
                        </p>\
                        <img src="static/default/imgs/smiley_herve.gif">\
                    </div>\
                    </center>\
                </div>').fadeIn(300);
        setTimeout(
            function() {
                $(".text").fadeOut(300, function() {
                    $('.text').html('Ravi de vous revoir !').fadeIn(300);
                    setTimeout(
                        function() {
                            $(".text").fadeOut(300, function() {
                                setTimeout(
                                    function() {
                                        if ("github" in user.profile){
                                        $.ajax({

                                            url: '/ajax/' + encodeURIComponent(user.profile.github.rss),
                                            type: 'GET',
                                            dataType: 'xml',
                                            error: function(xhr, status, e) {},
                                            success: function(feed) {
                                                var html = '';
                                                //log>feed;
                                                $(feed).find("entry").slice(0,5).each(function(i, e) {
                                                	//log>e;
                                                	//log>$(e).find("title").html();
                                                    html += `
                                                    <li>
                                                    	<a href="${$(e).find("link").attr("href")}">${$(e).find("title").html()}</a><br
                                                    </li>`
                                                });
                                                //log>html;
                                                html = "<h1>GitHub rss</h1><ul>" + html +"</ul>"
                                                $('#github').fadeOut(500);
                                                $('#github').html(html).fadeIn();
                                            }
                                        });
                                    }else{
                                        $('#github').hide();
                                    }
                                        $("#hello").fadeOut(300, function() {
                                            $(this).remove();
                                            $('.text-green').html(`
                                            <div class="container">
			                                	<div class="masonry" id="widgets">
                                                <content>
											        <div class="item">
											            <div class="card white shadows">
											                <div id="github" class="content">
											                     <center><img src="/static/default/imgs/loader.gif" /></center>
											                </div>
											            </div>
											        </div>
											        <div class="item">
											            <div class="card white shadows">
											                <div class="content">
											                    <h1>Activité</h1> 
											                </div>
											            </div>
											        </div>
											        <div class="item">
											            <div class="card white shadows">
											                <div class="content">
											                    <h1>Meteo</h1> 
											                </div>
											            </div>
											        </div>
											        <div class="item">
											            <div class="card white shadows">
											                <div class="content">
											                    <h1>Agenda</h1> 
											                </div>
											            </div>
											        </div>
                                                </content>
											    </div>
											 </div>
			                                	`).addClass('animated bounceInUp');
                                            ù();;
                                        })
                                    }, 0
                                );

                            })
                        }, 2000
                    );
                })
            }, 2000
        );
    } else {
        $('.text-green').hide().html('\
                    <div class="container"><center><p class="text-green" style="font-size: 50px;">Pour acceder à un dashboard vous devez etre connecté(e)</p></center></div>\
                <div id="connexion" class="container">\
                    <div class="card white shadows logincard">\
                        <div class="header"><h1>Connexion</h1></div>\
                        <form class="content" method="post" action="/connexion">\
                            <div>\
                                <input id="user" placeholder="Prénom" type="text" name="nom">\
                            </div>\
                            <div>\
                                <input placeholder="Mot de passe" type="password" name="code">\
                            </div>\
                            <input type="hidden" value="/dashboard" name="next">\
                            <button type="submit">Connexion !</button>\
                        </form>\
                        <div class="footer"><a style="color:#fff;" href="/inscriptions">Se créer un compte</a></div>\
                    </div>\
                </div>').fadeIn(300);
        
        $("#user").focus();
    }
});