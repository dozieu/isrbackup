# isrbackup
Concurrently access and backup Cisco router configuration files

Name: isrbackup
================
isrbackup allows user to backup running configuration of multiple Cisco devices without having to log into them individually. 
It is able to concurrently access multiple devices, retreive their running config and save to an "isr_backups" folder.


Overview
=========
Isrbackup is a Python script for accessing Cisco IOS devices.
The devices must support netconf:base:1.0 and ssh access.
This script employs the python ncclient and netmiko libraries

-Uses netmiko to configure netconf if required
https://pypi.org/project/netmiko/

-Uses nccleint to retrieve routers running configuration 
https://pypi.org/project/ncclient/

How to use
==========

Text file: You will need a text file listing the Ip address and hostname, seperated by space.
Text file format will be one ip address hostname pair per line e.g "10.10.10.10 hostname".
See sample file "samplefile.txt". File should be placed in same directory as isrbackup.py script.

This script will prompt user for the following:

- username and password:  this single username and password must have enable priviliges on all devices on your text file

- netconf port: you can set port that you want to use or that you have already configured for netconf, default is 22

- filename: name of your text file to use as input

- "Will you need to enable netconf?":  enter 'yes' script will configure netconf of the devices or 'no' if you have netconf already configured on devices






If you're asking why netconf ? -- No particular reason other than that I was learning the two packages for automating Cisco devices,
I am aware this can be done using netmiko alone. This script was a base for future scripts that may involve either package.

