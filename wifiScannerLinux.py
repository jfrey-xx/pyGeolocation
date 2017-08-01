###############################################################
#
# Main class is WifiGrab. No arguments required for initialization.
# When an object is created it executes a netsh command and stores the result
# in a semi-formatted manner
# The function all() uses this result to spit out SSIDs, BSSIDs and signal strength as
# lists
#
###############################################################

# NB: adapted for linux from code seen https://github.com/unwiredlabs/location-magic/pull/2
# FIXME: hard-coded interface

import subprocess
import os
import sys
import re

class WifiGrab:
    def __init__(self):

        #Check if running as ROOT
        if not os.geteuid() == 0:
            sys.exit('must be run as root because of use of network card')
        
        #Get Networks
        iw = ['iwlist', 'wlo1', 'scan']
        wlist = subprocess.Popen(iw, shell=False, stdout=subprocess.PIPE,)
        stdout_str = wlist.communicate()[0].decode('utf-8')

        self.results =  stdout_str.splitlines()  # Splitting the result of our netsh command into a list containing each line
        self.ssids = []
        self.bssids = []
        self.rssi = []
        self.channel = []

    def all(self):
        for line in self.results:
            line = line.strip()
            #Get BSSID 
            match = re.search('Address: (\S+)',line)
            if match:
               self.bssids.append(match.group(1))
    
            #Get Signal Strength
            match = re.search('Signal level=([0-9-]+) dBm',line)
            if match:
                self.rssi.append(match.group(1))
    
            #Get Channel Number
            match = re.search('Channel:([0-9]+)',line)
            if match:
                self.channel.append(match.group(1))
    
        # FIXME: empty ssids, not used later on
        return self.ssids, self.bssids, self.rssi, self.channel
