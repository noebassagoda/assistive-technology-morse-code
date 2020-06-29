let {PythonShell} = require('python-shell')

var path = require("path")
views = ["menu", "talk", "game", "email"]


function sendToPython() {

  var emailDirContent = document.getElementById("exampleFormControlInput1").value;
  var subjectContent  = document.getElementById("exampleFormControlInput2").value;
  var textContent     = document.getElementById("exampleFormControlTextarea1").value;
  
  var options = {
    scriptPath : path.join(__dirname, './../engine/util/scripts/'),
    args : [emailDirContent, subjectContent, textContent]
  }

  let pyshell = new PythonShell('email_script.py', options);


  pyshell.on('message', function(message) {
    if (message.indexOf("exito") > -1) {
      window.location.replace(`menu.html?alert=${encodeURIComponent(message)}`);
    }
  })

}

document.addEventListener('keypress', logKey);

function logKey(e) {
  var $focus = $(":focus").attr("id");

  if(e.which == 13) {
    e.preventDefault();
    sendToPython()
  }
}
