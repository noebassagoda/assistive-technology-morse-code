
window.$ = window.jQuery = require('jquery');
views = ["menu", "talk", "game", "email", "setup"]

var current_mode = 0;

$(document).on('keydown',function(e) {
  if(e.which == 13) {
    if ($(":focus")) {
      var $focus = $(":focus").attr("id");
      var newPath = views.indexOf($focus) > -1 ? `${$focus}.html` : null
      if (newPath) {
        window.location.replace(newPath);
      }
    }
  }

  if(e.which == 16) {
    e.preventDefault()
    current_mode = (current_mode + 1) % 2
    if (current_mode == 0) {
      $(instructions).html(
        `<span class="header-span">MODO NAVEGACION ACTIVADO.</span> 
        Presion el botón 1 para cambiar de modo, 2 moverte con el TAB al siguiente elemento,y 4 para 
          usar el ENTER`
      )
    }
    else {
      $(instructions).html(
        `<span class="header-span">MODO ESCRITURA ACTIVADO.</span> 
          Presion el botón 1 para cambiar de modo, 2 para simular un • , 3 para - y 4 para generar un ESPACIO`
      )
    }
  }

});

// $("#info-speed").on('keypress',function(e) {
//   if(e.which == 13) {
//     hidden = $("#info-speed-content").hasClass("instructions-hidden")
//     if (hidden) {
//       $("#info-speed-content").removeClass("instructions-hidden")
//     }
//     else{
//       $("#info-speed-content").addClass("instructions-hidden")
//     }
//   }
// })

$.urlParam = function(name) {
	var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
  var param = results ? results[1] : 0
  return param;
}

$(document).ready(function(){
  alert_message = $.urlParam("alert")
  if (alert_message) {
    $("#alert-box").append(decodeURIComponent(alert_message))
    $("#alert-box").removeClass("hidden-alert")
    setTimeout(function() {
      $("#alert-box").addClass("hidden-alert");
    }, 6000);
  }

  $("#minus,#plus").on('keypress',function(e) {
    if(e.which == 13) {
      e.preventDefault()
      var value = parseFloat($("#morse-speed").val());
      var addValue = $(this).is("#minus") ? -0.1 : 0.1
      $("#morse-speed").val((Math.round((value + addValue) * 100) / 100).toFixed(2));
    }
  });
})
