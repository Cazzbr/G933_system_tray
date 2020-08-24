# G933_system_tray
System tray indicator for <a href="" target="_blank">G933-utils</a> by <a href="https://github.com/ashkitten" target="_blank">ashkitten</a>
# Disclaimer
The app indicatior is written in python3.
This app is only a system tray application to show the battery level of the G933 headset. It must work on any device supported by the command line utility, but the name of the app will not change based on that.

# Instalation
* First off all you need to install the <strong>ashkitten G933-utils</strong>, download and install It from his Github repo;
* You must also have to add It to your $PATH;

When the g933-utils is working on the command line and added to PATH, you just need to download the script and the media folders and execute it.
I plan to add more detalied info on how to do it when de app is more polished, but if you have basic linux knowledge this will be straightforward.

# Known Issues
For now, if you have the usb stick plugged and the headset turned off the app will freeze (It will not responding eather to click on it or `ctrl+c` on the terminal).
The work around for now is to turn the headset on or remove the usb stick to be able to terminate the app.
