function openNav() {
    document.getElementById("sidenav").style.width = "250px";
    //document.getElementById("content").style.marginLeft = "250px";
    //document.getElementById("nav").style.marginLeft = "215px";
    document.getElementById("content").style.filter = "blur(10px)";
       
}

function closeNav() {
    document.getElementById("sidenav").style.width = "0";
    //document.getElementById("content").style.marginLeft = "0";
    //document.getElementById("nav").style.marginLeft = "0px";
    document.getElementById("content").style.filter = "blur(0px)";
}

$( document ).ready(function() {

  $("#content").click(function(){
        closeNav();
    }); 

  $("#nav-button").click(function(){
    openNav();
  });

  $(".dropdown-btn").click(function(){
    if(this.getAttribute('data-status') == null || this.getAttribute('data-status') == "close" ){
      $(this).attr("data-status","open");
      p = $(this).position();
      s = $("#"+this.getAttribute('data-action'));
      s.css("display","block");
      s.css("top",p.top + 70);
      s.css("left",p.left - 300 + 40);
    }else{
      $(this).attr("data-status","close");
      s = $("#"+this.getAttribute('data-action'));
      s.css("display","none");
    }
    
  });

  $('.search input').keypress(function (e) {
    if (e.which == 13) {
      $('.search form').submit();
      return false;
    }
  });

  


});