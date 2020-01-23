# hm-python-bt-scaffold

# README #

### Overview  ###

This sample app for python bluetooth shows the basic use of Python HMKit to authenticate with the car emulator, send and receive a command through bluetooth.

### Where to find supporting documentations? ###

Developer Center:
https://developers.high-mobility.com/

Getting Started with Python Bluetooth Beta SDK:
https://high-mobility.com/learn/tutorials/sdk/python/

Code References:
https://high-mobility.com/learn/documentation/iot-sdk/python/hmkit/

### Configuration ###

Set Python 3.7 as default in alternatives.
Install python hmkit on the "Raspberry Pi Zero W" board.

Install python hmkit from github repo:
https://github.com/highmobility/hmkit-python

Before running the app, make sure to configure the following in the app:

1. Initialise hmkit with a valid Device Certiticate from the Developer Center https://developers.high-mobility.com/
2. Find the Access Token in respective emulator from https://developers.high-mobility.com/ and paste it in the source code to download Access Certificates from the server.

### Run the app ###

Disable system default Bluetooth software elements (run once per reboot)
$./sys_bt_off.sh

Run the app on your pi zero W board, to see the basic flow:

1. Initialising the SDK
2. Getting Access Certificates
3. Bluetooth Connecting and authenticating with an emulator
4. Sending and receiving commands

$./scaffold/app.py
Pi zero W device need internet access to be able to download Access Certificate.

### Questions or Comments ? ###

If you have questions or if you would like to send us feedback, join our Slack Channel or email us at support@high-mobility.com.
