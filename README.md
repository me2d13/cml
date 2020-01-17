# Intro
This repository contains set of tools which can send commands (coded in python) to mqtt server. Typical usage (for author) is local home network with mqtt messaging used for home automation.

Suppose you can control lights, heating, jalousies by mqtt messages. Then you can benefit of __numbered commands__ which will send typical actions for your home. Numbered commands may look old school for fancy modern responsive UIs, but it's easy to build hardware device with keypad to enter such commands.

So with these tools you can for example define command number 13 which opens garage doors, waits 2 minutes and then closes the doors. Such command can be entered from web page, mobile phone or hw gadget.

# Components
* __server__ python program which
  * defines the commands (using delays, threading, mqtt library and whatever you need)
  * has some coordination logic to detect and execute those commands. Coordinates threads for running commands (with delays)
  * has build in http server to receive inputs from web/android app
* __cml-web__ is very simple react application which displays keypad to enter numeric commands. This application is intended to run at internal network only. Making it available for public internet would require additional authentication which I'm too lazy to implement (as I don't need it)
* __cml-mobile__ android application which displays keypad to enter the commands. Here the extended authentication is in place. The android app uses JWT to authenticate itself and as such need to be registered as client for server. Server keeps track of known clients. _NOT IMPLEMENTED YET_
* __cml-keypad__ code for Wemos D1 (ESP8266) with simple matrix keyboard. Intended to be connected to you local wifi and mounted to wall at your home or used as battery powered device. _NOT IMPLEMENTED YET_

See RADMEs in each component's folder for details

# Web server config
I need to add nice picture here. But what I use: _Server_ runs as Python docker container available at internal network. In another container there's Nginx web server listening at port 80 which is port-triggered from internet router. So until _cml-mobile_ is in place and server API needs to be accessed from public net the Nginx __won't__ proxy traffic to the _server_. But Nginx is used as server for _cml-web_ to be accessible from internal network. Just runs at different port (different virtual server).