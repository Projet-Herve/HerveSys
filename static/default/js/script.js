  function sleep(delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
  }
  
function openNav() {
    document.getElementById("sidenav").style.width = "250px";
    //document.getElementById("content").style.marginLeft = "250px";
    //document.getElementById("nav").style.marginLeft = "215px";
    //document.getElementById("content").style.backgroundColor = "rgba(0,0,0,0.4)"; 
    
    
}
/* Set the width of the side navigation to 0 and the left margin of the page content to 0, and the background color of body to white */
function closeNav() {
    document.getElementById("sidenav").style.width = "0";
    //document.getElementById("content").style.marginLeft = "0";
    //document.getElementById("nav").style.marginLeft = "0px";
    //document.getElementById("content").style.backgroundColor = "#E6E6E6";
}

function checkSubmit(e) {
   if(e && e.keyCode == 13) {
      document.forms[0].submit();
   }
}