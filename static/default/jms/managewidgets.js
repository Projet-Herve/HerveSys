$(function() {
    $('.new').click(function (event){
         log>encodeURIComponent($(this).attr('data-what'));
         $.get({
            url: "/active/widget",
            data : {what :$(this).attr('data-what')},
            success: function(response) {
                location.reload();
            }
         })
         return false;
    });
     $('.del').click(function (event){ 
         event.preventDefault(); 
         $.get({
            url: "/desactive/widget",
            data : {what :$(this).attr('data-what')},
            success: function(response) {
                location.reload();
            }
         })
         return false;
});
     });