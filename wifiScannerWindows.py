###############################################################
#
# Main class is WifiGrab. No arguments required for initialization.
# When an object is created it executes a netsh command and stores the result
# in a semi-formatted manner
# The function all() uses this result to spit out SSIDs, BSSIDs and signal strength as
# lists
#
###############################################################
import subprocess

class WifiGrab:
    def __init__(self):
        self.results = subprocess.check_output(["netsh", "wlan", "show", "all"])  # netsh command. Try it on CMD to examine the output
        self.results = self.results.replace("\r", "")
        self.results = self.results.split("\n")  # Splitting the result of our netsh command into a list containing each line
        self.ssids = []
        self.bssids = []
        self.rssi = []
        self.channel = []

    def all(self):
        x = 0  # For traversing self.results
        while x < len(self.results):
            if self.results[x].split(" ")[0] == 'SSID':  # When we reach a line
                # which lists properties about a certain SSID
                ssidLine = self.results[x]
                ssidLineSplit = self.results[x].split(': ')
                self.ssids.append(ssidLineSplit[len(ssidLineSplit) - 1])

                bssidLine = self.results[x + 4]
                bssidLineSplit = self.results[x + 4].split()
                self.bssids.append(bssidLineSplit[len(bssidLineSplit) - 1])

                rssiLine = self.results[x + 5]
                rssiLineSplit = self.results[x + 5].split()
                rssi = rssiLineSplit[len(rssiLineSplit) - 1]  # this value is actually signal quality in percentage
                rssi = int(rssi[:len(rssi) - 1])  # Drop the percentage sign and convert to int
                rssi = (rssi/2) - 100  # actual RSSI value
                self.rssi.append(rssi)

                channelLine = self.results[x+7]
                channelLineSplit = channelLine.split()
                channel = channelLineSplit[len(channelLineSplit)-1]
                self.channel.append(channel)
            x += 1
        return self.ssids, self.bssids, self.rssi, self.channel