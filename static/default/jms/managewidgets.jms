$(function() {
    $('.new').click(function (event){ 
         event.preventDefault(); 
         $.ajax({
            url: $(this).attr('href')
            ,success: function(response) {
                location.reload();
            }
         })
         return false; //for good measure
    });
     $('.del').click(function (event){ 
         event.preventDefault(); 
         $.ajax({
            url: $(this).attr('href')
            ,success: function(response) {
                location.reload();
            }
         })
         return false; //for good measure
    });
});