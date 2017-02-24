
function update(widget){
    if ($(window).width() < 601){ 
    // smal screen
        $("#widgets").append('<div class="item"><div id="'+widget["element"].slice(1, -1)+'"><center><img src="/static/default/imgs/loader.gif"/></center></div></div>').addClass('animated fadeInUp')
    }else{
        $("#widgets").append('<div class="item"><div id="'+widget["element"].slice(1, -1)+'"><center><img src="/static/default/imgs/loader.gif"/></center></div></div>')

    }
    $.get(widget["url"], function(datas) {
        var html = $('<div/>').append(jQuery.parseHTML(datas)).find(widget["element"]).html();
        if (html != undefined){
            $("#"+widget["element"].slice(1, -1)).html(html);
        }
    });
}
$(function() {
    $.get("/list/widgets", {}, function(widgets) {
        for(var i = 0; i< widgets.length; i++) {
            widget = widgets[i].split(" ");
            widget = {
                    "element": widget[0],
                    "url": widget[1]
                }
            update(widget);
        }
    });
});