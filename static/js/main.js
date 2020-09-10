function mobileTopMenu() {
    var x = document.getElementById("Topnav");
    if (x.className === "topnav") {
      x.className += " responsive";
    } else {
      x.className = "topnav";
    }
  } 
function mobileMidMenu() {
    var x = document.getElementById("midnav");
    if (x.className === "midnav") {
      x.className += " responsive";
    } else {
      x.className = "midnav";
    }
  }