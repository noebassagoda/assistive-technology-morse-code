let {PythonShell} = require('python-shell')

var path = require("path")
views = ["menu", "talk", "game", "email"]


function sendToPython() {

  var textContent = document.getElementById("textAreaTalk").value
  
  var options = {
    scriptPath : path.join(__dirname, './../engine/util/scripts/'),
    args : [textContent]
  }

  let pyshell = new PythonShell('voice_script.py', options);


  pyshell.on('message', function(message) {
    document.getElementById("textAreaTalk").value = "";
  })

}

document.addEventListener('keypress', logKey);
var myVar;


function myTimer() {
  sendToPython()
}

function logKey(e) {
  if (myVar) {
    clearInterval(myVar);
  }
  var $focus = $(":focus").attr("id");

  if (views.indexOf($focus) === -1) {
    myVar = setTimeout(myTimer, 3000);
  }
}
