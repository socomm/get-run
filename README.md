# Overview #

**get-run** is an Open-Source software designed to help extract Cisco running 
config from SSH enabled cisco hardware - namely routers and switches.

# License #

GPLv3, with full license available in LICENSE file.

# Requirements and Dependencies #

This program requires the following python modules:

    - paramiko
    - getpass
    - click
    - ipaddress
    - signal
    - sys

# Planned features # 

	- Retrieve running-config via ssh
	- Backups+Scheduler
	- Config Deployments
	- Config rollback
	- Security (diff configurations, ARP)
	- E-Mail notification
