import requests
import json
import subprocess
import googlemaps
import decimal

geolocateApiKey="<YOUR API KEY>"

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


class geolocate:
    def __init__(self, key=geolocateApiKey):
        global geolocateApiKey

        self.key = key
        self.url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + self.key
        self.gmaps = googlemaps.Client(key=self.key)  # For reverse geocoding google geolocation response


        self.response = []
        self.payload = {}

        self.WifiObject = WifiGrab()  # to grab BSSIDs
        self.ssids, self.bssids, self.rssi, self.channel = self.WifiObject.all()

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
            self.payload['wifiAccessPoints'][i]['signalStrength'] = self.rssi[i]
            self.payload['wifiAccessPoints'][i]['channel'] = self.channel[i]

        self.headers = {
            'content-type': 'application/json',
        }
        # Payload structure reference: https://developers.google.com/maps/documentation/geolocation/intro#body

    def importJSON(self):  # Import JSON payload from file
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
        self.key = key

    def printResponse(self):
        try:
            print self.getResponse()
        except Exception, e:
            print str(e)

    def getPayload(self):
        return self.payload

    def getResponse(self):
        return json.loads(self.response.text)

    def getLongLat(self):
        response = json.loads(self.response.text)
        decimal.getcontext().prec = 15  # Setting precision for lat/lng response
        lng = decimal.Decimal(response['location']['lng']) + 0
        lat = decimal.Decimal(response['location']['lat']) + 0
        return lat, lng

geolocateMe = geolocate(geolocateApiKey)    # replace geolocateApiKey variable at the top with your API key
geolocateMe.buildJSON()                     # build JSON request object
geolocateMe.request()                       # Send request to google
geolocateMe.printResponse()                 # Print response from google
geolocateMe.getLongLat()