#!/usr/bin/env python
"""
get-run is a small script to help connect to a given Cisco device, by IP
address, and retrieve its running config.

Copyright (C) 2015-Present Juan Espinoza <juan@espinoza.cc>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import paramiko             # SSH connectivity
import getpass              # Get user-password interactively
import sys                  # System calls
import argparse             # Parse CLI arguments
import ipaddress            # Validate IP address
import signal               # Catch keyboard interrupts
import click                # Replacing argparser

#--{  get_params  }-------------------------------------------------------------
def get_params():
    """
    This function uses argparse and getpass in order to parse through user
    input for IP address, username, and password.
    """
    gr_parser = argparse.ArgumentParser(description='CLI args.')
    gr_parser.add_argument('-H', dest='host', required=True,
    help='Specify hostname or IP Address.')
    gr_parser.add_argument('-u', dest='user', required=True,
    help='Specify username.')

    # Convert args to a dictionary for easier accessibility
    tmp = vars(gr_parser.parse_args())

    # Convert to unicode format - for use with the ipaddress module
    ip_address = unicode(tmp['host'], "utf-8")

    # Validate IP address - Error out if invalid value
    try:
        ipaddress.ip_address(ip_address)
    except ValueError:
        sys.exit("E: Invalid IP address: "+ip_address)

    user = tmp['user']
    pswd = getpass.getpass(stream=sys.stderr, prompt="Password: ")
    return ip_address, user, pswd
#-------------------------------------------------------------{  get_params  }--

#--{  ssh_conn  }---------------------------------------------------------------
def ssh_conn(host, user, pswd):
    """
    This function takes 3 parameters, used for connecting to the Cisco devices.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    port = 22

    # Catch any exceptions connecting to host.
    try:
        ssh.connect(host, port, user, pswd, allow_agent=False,
        look_for_keys=False, timeout=3)
    except:
        sys.exit("E: Unable to connect to: "+host)

    # Catch any exceptions running commands on host.
    try:
        (stdin, stdout, stderr) = ssh.exec_command("show running-config")
    except:
        sys.exit("E: Could not run command on: "+host)

    print stdout.read()
    ssh.close()
#---------------------------------------------------------------{  ssh_conn  }--

if __name__ == '__main__':
    HOST, USER, PSWD = get_params()
    ssh_conn(HOST, USER, PSWD)
