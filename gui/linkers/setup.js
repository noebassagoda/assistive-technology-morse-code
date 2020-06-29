let {PythonShell} = require('python-shell')
window.$ = window.jQuery = require('jquery');

var path = require("path")
views = ["menu", "talk", "game", "email"]


function sendToPython() {

  var email = document.getElementById("exampleFormControlInput1").value;
  var password = document.getElementById("exampleFormControlInput2").value;
  var speed  = document.getElementById("morse-speed").value;

  var options = {
    scriptPath : path.join(__dirname, './../engine/util/scripts/'),
    args : [email, password, speed]
  }

  let pyshell = new PythonShell('setup_script.py', options);


  pyshell.on('message', function(message) {
    if (message.indexOf("exito") > -1) {
      window.location.replace(`menu.html?alert=${encodeURIComponent(message)}`);
    }
  })

}

function receivePython() {
  var options = {
    scriptPath : path.join(__dirname, './../engine/util/scripts/'),
    args : []
  }

  let pyshell = new PythonShell('retrieve_config_script.py', options);

  pyshell.on('message', function(message) {
    var config = JSON.parse(message)
    document.getElementById("exampleFormControlInput1").value = config["email"]
    document.getElementById("exampleFormControlInput2").value = config["password"]
    document.getElementById("morse-speed").value = config["speed"]
  })
}

$(document).ready(function(){
  receivePython()
})



document.addEventListener('keypress', logKey);

function logKey(e) {
  var $focus = $(":focus").attr("id");

  if ($focus == "submit-btn") {
    e.preventDefault();
    sendToPython()
  }
}
