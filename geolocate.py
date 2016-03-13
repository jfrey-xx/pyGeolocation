import requests
import json
import subprocess

geolocateApiKey="<YOUR API KEY>"

class WifiGrab:
    def __init__(self):
        self.results = subprocess.check_output(["netsh", "wlan", "show", "all"])  # netsh command. Try it on CMD to examine the output
        self.results = self.results.replace("\r", "")
        self.results = self.results.split("\n")  # Splitting the result of our netsh command into a list containing each line
        self.ssids = []
        self.bssids = []
        self.signals = []

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

                signalLine = self.results[x + 5]
                signalLineSplit = self.results[x + 5].split()
                signal = signalLineSplit[len(signalLineSplit) - 1]
                self.signals.append(int(signal[:len(signal) - 1]))
            x += 1
        return self.ssids, self.bssids, self.signals


class BuildGoogleObject:
    def __init__(self, key=geolocateApiKey):
        global geolocateApiKey

        self.key = key
        self.url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + self.key

        self.response = []
        self.payload = {}

        self.WifiObject = WifiGrab()  # to grab BSSIDs
        self.ssids, self.bssids, self.signals = self.WifiObject.all()

    def buildJSON(self):
        if len(self.bssids) < 3:
            print 'Atleast two BSSIDs are required.'
            print 'Current number of bssids: %i' % len(self.bssids)
            return

        # Building payload as per google-guidelines
        self.payload['considerIp'] = 'true'
        self.payload['wifiAccessPoints'] = []
        for i in range(0,len(self.bssids)):
            self.payload["wifiAccessPoints"].append({})
            self.payload['wifiAccessPoints'][i]['macAddress'] = self.bssids[i]

        self.headers = {
            'content-type': 'application/json',
        }
        # Payload structure reference: https://developers.google.com/maps/documentation/geolocation/intro#body

    def importJSON(self):
        self.payload = json.load(open("geolocate.json"))
        self.headers = {
            'content-type': 'application/json',
        }

    def request(self):  # Send request to geolocate and return the response
        try:
            self.response = requests.post(self.url, data=json.dumps(self.payload), headers=self.headers)
        except Exception, e:
            print str(e)

    def replaceKey(self, key):  # Replace geolocate API key
        self.url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + key

    def printResponse(self):
        try:
            print json.loads(self.response.text)
        except Exception, e:
            print str(e)

geolocateObject = BuildGoogleObject(geolocateApiKey)  # replace geolocateApiKey variable at the top with your API key
geolocateObject.buildJSON()  # build JSON request object
geolocateObject.request()    # Send request to google
geolocateObject.printResponse()  # Print response from google