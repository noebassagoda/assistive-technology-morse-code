Assistive Technology Device Using Morse Code
======
_Created with ❤️ by [María Noel Bassagoda](https://github.com/nbassagoda)_  
_It is recommended to check out the following [presentation](https://www.canva.com/design/DAEAsMVapFs/nRLMMbAQ4XeFwofrsamfEg/view?utm_content=DAEAsMVapFs&utm_campaign=designshare&utm_medium=link&utm_source=sharebutton#1) to get a brief overview of what this project is about._

The idea of this project is to take advantage of the use of morse code as an alternative to the computer keyboard, and together with a set of contact sensors develop an application that allows access to certain computer functionalities (potentially achieving full access to the computer). One of the advantages of this project lies in the possibility to arrange the buttons in the way that suits you the most; being able to even build a device with these buttons, and adapt it to the needs of each one.

The general idea of the project consists of 2 applications: a Python application that handles the processing of morse code and a web application that provides a graphical interface to the application. In this case, it was used a [USB4butiá board](https://www.fing.edu.uy/inco/proyectos/butia/mediawiki/index.php/USB4butiá) with 4 buttons, but you can easily adapt this project to use the board and buttons of your choice due to the modulated design of the app.

## Table of Contents

- [Motivation](#motivation-)
- [Architecture](#architecture-)
  - [Python App](#python-app)
  - [User Interface](#user-interface)
- [Mounting the device](#mounting-the-device-)
- [Getting Started](#getting-started-)
  - [Previous Requirements](#previous-requirements)
  - [Installation](#installation)
- [Demo](#demo-)
- [Future Work](#future-work-)
## Motivation 💡

At the time of its invention, morse code definitely changed the way we communicate. Historically, it has been used in nautical navigation, from aviation to radio, but it is still easy to learn and its universal nature makes it an excellent data entry method for use as assistive technology.

Morse code has several advantages over other alternative computer access strategies. It is generally faster and requires a less fine control motor. Perhaps its most important advantage is its ability to become a sub-cognitive process. After using it for a while, a morse code user no longer thinks about the code they are entering. This is the same process that typists use and has a significant impact on the speed, accuracy, and quality of the work that is produced. Speeds of between 15 and 30 words per minute are common and speeds of over 60 words per minute can be achieved, making it a very efficient data entry alternative.

Currently, this technology is widely used in the area of assistive technology, some mobile phones even support data entry from morse code natively, but without a doubt the most used option today is the Google keyboard (Gboard). It provides a data entry method from morse code and allows full control of the device from it. Google even has a collection of experiments, known as [Hello Morse](https://experiments.withgoogle.com/collection/morse), where it encourages users to make devices to empower the use of morse code as assistive technology.

## Architecture 🛠
The app has the backend developed in [Python](https://www.python.org/) that handles the processing of morse code entered by the user and a desktop app developed in [Electron](https://www.electronjs.org/). 

Nowadays, modern browsers (and therefore, desktop apps based on web apps, like in our case) support the usage of focus indicators triggered by the keyboard that facilitates the navigation through interactive elements on a web page as long as the current page supports it. In our case, the app was developed to support this functionality, facilitating the navigation using the buttons attached to the board. You can read more about these techniques [here](https://webaim.org/techniques/keyboard/).

This app strongly relies on the functionality mentioned before, which in our case, will be simulated keystrokes generated by the buttons attached to the board. The keystrokes that will be simulated are mainly the **TAB** and **SHIFT+TAB** commands to navigate through the interactive elements on the screen, as well as the **ENTER**. 

#### Python App
The backend is developed in Python, for which there is an app running in the background, translating the button strokes into keyboard events. There are 2 main data entry modes:

  - Navigation mode: when this mode is activated, the keystrokes are translated into keyboard events related to the navigation within app. One button translates into a **TAB** stroke to navigate to the next element on the page, another button translates to **SHIFT + TAB** that is used to navigate to the previous element within the page, and another button that translates into an **ENTER**). Potentially, more shortcuts could be configured that allow greater navigability within the browser.

  - Writing mode: there are 2 buttons that are mapped one with *•* and another with **-** as stated in morse code. Then the sequence of *•* and **-** will be mapped to the corresponding letter according to the morse code alphabet. Additionally, a 3rd button will be used in order to trigger the event of the space-bar.


#### User Interface

This application provides a friendly interface for the user through a desktop application developed with ElectronJS (which in the background is based on a web application). Like we mentioned before, we will use keyboard shortcuts to navigate through the interactive elements of the app with the keyboard. The functionalities developed were the following:

  - **Send emails**. It is done in conjunction with a Python script that is in charge of sending the mail with the content that was entered in the web app)

  - **TTS** (text to speech) functionalities. It is also done together with a Python script that uses the GTTS library to generate audio from the string that is entered in the web app through the sensor buttons in morse code, then automatically play said audio and finally delete it)

  - A section to configure **general settings**, such as the writing speed and the corresponding email and password for using the email functionality
  
  - An interactive section to **learn Morse Code**.

  - **Audio response system** both when changing the button mode (an audio is played indicating the new mode in which we are) and also when writing in morse code. For this, when the application translates a sequence of characters (made up of dots and dashes) in a keyboard event, not only will it trigger the corresponding keyboard event but will also play the sound of a keystroke to give the user notion that a sequence was registered correctly. In the event that a sequence is entered that does not correspond to any character recognized by the program, neither the keyboard events nor the sound of any keystroke will be generated.

## Mounting the Device 🤖
Nowadays, several types of morse input are currently supported:

  - Simple switch, where a dash differs from a point by holding the switch depressed for a longer period of time
  - Dual switch where one switch is used to enter points while the other is used for hyphens
  - Triple switch, where one switch is used to enter a period, one for a dash, and the third to indicate the end of the character or command performed.

In this project, we use an adaptation of this last method, where 3 switches are used for the translation of morse code, and a fourth switch is also added to facilitate navigation functionalities.

#### Materials
- USB4butia board
- 4 push buttons
- 4 RJ45 sensor cables
- USB cable
- Double-sided tape (optional for button mounting)

To assemble the device, all you have to do is connect the button sensors to the board and then the board to the computer. In my case, I simply glued the buttons to a plate with double-sided tape, but the idea is that each one adapts it according to their needs. The versatility of the 4 buttons allows them to be arranged most conveniently for each one. In the following diagram you'll see an example of how it should be arranged by default (for the code to work out of the box):


<p align="center">
<img width="883" alt="Screen Shot 2020-12-12 at 12 25 34 PM" src="https://user-images.githubusercontent.com/27690774/101987822-2e444b80-3c75-11eb-9417-87d574bcf8fd.png">
</p>


## Getting Started 🚀

#### Previous Requirements
Before running the app, you should install the following packages:

- Homebrew
- Python
- Pip
- Virtualenv
- Node

#### Installation
Once the previously mentioned packages have been installed, we continue to install the project. For this, we will first clone this repo and run the following commands:

```
$cd assistive-technology-morse-code
$python -m virtualenv env
$source env/bin/activate
$pip install -r requirements.txt
$npm install
```

#### Start the Server
Once everything is correctly installed, we are all set to run the application. For this we will have to run the background process that handles the action of the buttons and the desktop app:

```
$cd engine
$python main.py
```

Finally, we open another console tab and run the following command to start the desktop app:

```
$npm start
```

#### Configure Email
You should configure the permissions and credentials of the email in order to make use of this functionality. First things first, you should enable third-party applications to send emails on your behalf since we will be sending emails from a python script. This step may not be necessary depending on the email service used, you can see in the following [video](https://youtu.be/6wWKa0hdd3M) how to do so.

#### Accessibility settings
If you are using mac OS Mojave or newer, there is a new security feature where applications must be explicitly allowed to trigger mouse / keyboard events (in our case, we want to fire keyboard events from the command line running the background process). To enable this, we must go to Security Preferences> Security and privacy> Privacy> Accessibility and choose from there to the command line application. Here's how to do it:

<p align="center">
<img width="400" src="https://user-images.githubusercontent.com/27690774/101991545-2b088a00-3c8c-11eb-9eea-3c55d1ab5458.png">
<img width="400" src="https://user-images.githubusercontent.com/27690774/101991549-2fcd3e00-3c8c-11eb-862d-22d3ce21b7d6.png">
</p>

#### You're all set! 💃 🥳 🚀


## Demo 🤩

You can find the following demos:
- [TTS demo](https://youtu.be/asNYsBEba9g)
- [Interactive Section](https://youtu.be/h3PfM4QIIcI)
- [Send Emails](https://youtu.be/FOEAoWcf6ec)
- [Configuration Section](https://youtu.be/JHPJrFPn3k0)

## Future work
This project is very versatile and can be adapted to your own needs. In particular, the application is modulated enough to be able to connect it to any board or device you want to sense with. For this, the only thing that has to be changed is the way in which we recover the state of the button used to sense. You can handle this in the following file: `assistive-technology-morse-code/engine/util/buttons_helper.py`.
