$(function() {
    $.get("/list/musique", {}, function(datas) {
        log>datas;
        for (var i = 0; i < datas.length; i++) {
            $(`<p href=\"#\" class=\"musique-item\" data-val=\"${datas[i]}\">${datas[i]}</p>`).hide().appendTo("#vosmusiques > .content").fadeIn(1000);
            //$("<hr>").hide().appendTo("#vosmusiques > .content").fadeIn(1000);
        }

        $('.musique-item').click(function() {
            file = $(this).data('val');
            $("#musique-status").html(`Lecture de ${file} <br><figure id="audioplayer">
                                                    <audio class="player" autoplay controls src="get/musique/${file}" id="audiotrack"></audio>
                                                </figure>`);
        });
    });
});
