window.$ = window.jQuery = require('jquery');
var classes = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

// generate likes
for (var i = 0; i < 9; i++) {
  $(".emoji-like").append(`
    <div class="emoji ${classes[i]} first-row emoji--like">
      <div class="emoji__hand">
        <div class="emoji__thumb"></div>
      </div>
    </div>`
  )
}

// generate hearts
for (var i = 0; i < 9; i++) {
  $(".emoji-love").append(
    `<div class="emoji ${classes[i]} first-row emoji--love">
      <div class="emoji__heart"></div>
    </div>`
  )
}

// generate laugh
for (var i = 0; i < 9; i++) {
  $(".emoji-laugh").append(
    `<div class="emoji ${classes[i]} first-row emoji--haha">
      <div class="emoji__face">
        <div class="emoji__eyes"></div>
        <div class="emoji__mouth">
          <div class="emoji__tongue"></div>
        </div>
      </div>  
    </div>`
  )
}

// generate yay
for (var i = 0; i < 9; i++) {
  $(".emoji-yay").append(
    `<div class="emoji ${classes[i]} first-row emoji--yay">
      <div class="emoji__face">
        <div class="emoji__eyebrows"></div>
        <div class="emoji__mouth"></div>
      </div>
    </div>`
  )
}

// generate wow
for (var i = 0; i < 9; i++) {
  $(".emoji-wow").append(
    `<div class="emoji ${classes[i]} first-row emoji--wow">
      <div class="emoji__face">
        <div class="emoji__eyebrows"></div>
        <div class="emoji__eyes"></div>
        <div class="emoji__mouth"></div>
      </div>
    </div>`
  )
}

// Generate letters
var letters = [
  ["a", "b", "c", "d", "e", "f", "g"],
  ["h", "i", "j", "k", "l", "m", "n"],
  ["o", "p", "q", "r", "s", "t", "u"],
  ["v","w","x","y","z"]
]

var morseAlphabet = 
  {'a': '.-', 'b': '-...', 'c': '-.-.',
   'd': '-..', 'e': '.', 'f': '..-.',
   'g': '--.', 'h': '....', 'i': '..',
   'j': '.---', 'k': '-.-', 'l': '.-..',
   'm': '--', 'n': '-.', 'o': '---',
   'p': '.--.', 'q': '--.-', 'r': '.-.',
   's': '...', 't': '-', 'u': '..-',
   'v': '...-', 'w': '.--', 'x': '-..-',
   'y': '-.--', 'z': '--..'}

for (var i = 0; i < 4; i++) {
  for (var j = 0; j < 7; j++) {
    var currentLetter = letters[i][j]

    if (i == 3 && (j == 5 || j == 6)) { break; }
    $(`#row-${classes[i]}-alphabet`).append(
      `<li tabindex=-1 id="alphabet-${currentLetter}">
        <a tabindex="-1" href="#">
          <p class="alphabet">${currentLetter.toUpperCase()}</p>
          <p class="morse-text">${morseAlphabet[currentLetter]}</p>
        </a>
      </li>`
    )
  }
}


$(document).on('click',function(e) {
  if ($(".emoji:first").hasClass("hidden")){
    $(".emoji").removeClass("hidden")
    setTimeout(function(){
      $(".emoji").addClass("hidden")
    },6000);
  }
})

$(document).ready(function(){
  abc = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
  ]

  emojis = [
    "love",
    "like",
    "laugh",
    "yay",
    "wow",
  ]

  var lettersCount = 0;
  var modal = document.getElementById("myModal");

  $(document).on('keypress',function(e) {
    var keyCode = e.which - 97
    var letter = abc[keyCode]
    var keyInAlphabet = keyCode >= 0 && keyCode < 26;
    
    if(keyInAlphabet) {
      var isAnimated = $(`#alphabet-${letter}`).is('[class^="animate-"]');
      if (!isAnimated) {
        // Count amount letters correct
        lettersCount ++;

        //Animate letter
        var randVal = Math.floor((Math.random() * 8) + 1);
        $(`#alphabet-${letter}`).addClass(`animate-${randVal}`)
        
        // Show emojis or completed animation
        var hiddenEmojisCount = $(".emoji-section, .hidden").length
        if (hiddenEmojisCount > 9 && lettersCount < 26) {
          var randEmoji = emojis[Math.floor((Math.random() * 4))];
          $(`.emoji-${randEmoji}`).removeClass("hidden")
          setTimeout(function(){$(`.emoji-${randEmoji}`).addClass("hidden")}, 5250);
        } 
        else if (lettersCount == 26) {
          modal.style.display = "block";
          $('document').off('keypress');
          $(document).on('keypress',function(e) {
            $("#go-back")[0].click();
          })
        }
      }
    }
  })
})
