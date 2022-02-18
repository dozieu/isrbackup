# isrbackup
Concurrently backup Cisco router configuration files

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

Try the dockerized web gui version https://hub.docker.com/r/dozieu/collabtools-v01

How to use
==========

Text file: You will need a text file listing the Ip address and hostname, seperated by space.
Text file format will be one ip address hostname pair per line e.g "10.10.10.10 hostname".
See sample file "samplefile.txt". File should be placed in same directory as isrbackup.py script.
script can be run with CLI arguments, esle srcipt will default to CLI prompts to guide user.

    usage: pub_isr_backup.py [-h] [-f str] [-p str]

    Pings IP addresses entered or from file

    optional arguments:
      -h, --help          show this help message and exit
      -f str, --file str  Input file - listing device name and ip address pairs
                          (default: None)
      -p str, --port str  netconf port number (default: None)


This script will prompt user for the following:

- username and password:  this single username and password must have enable priviliges on all devices on your text file

- netconf port: you can set port you have already configured for netconf, or leave blank to default to 22

- filename: name of your text file to use as input

- "Will you need to enable netconf?":  enter 'yes' script will configure netconf on the devices or 'no' if you have netconf already configured on devices






why netconf ? no particular reason other than that I was learning the two packages for automating Cisco devices,
I am aware this can be done using netmiko alone. 
