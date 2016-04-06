import requests
import json
import googlemaps
import decimal
from sys import exit as sysExit
import argparse
from reverseGeocode import ReverseGeocode
import wifiScannerWindows
import myMap

parser = argparse.ArgumentParser(prog='python geolocate.py')
parser.add_argument('geolocateApiKey', help='Your Geolocate API key. \nGet it from here: https://developers.google.com/maps/documentation/geocoding/get-api-key#key')
parser.add_argument('googlemapsApiKey', help='Your google maps ALI key')
args = parser.parse_args()

geolocateApiKey=args.geolocateApiKey
googlemapsApiKey=args.googlemapsApiKey

class geolocate:
    def __init__(self, key=geolocateApiKey):
        global geolocateApiKey

        self.key = key
        self.url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + self.key
        self.gmaps = googlemaps.Client(key=self.key)  # For reverse geocoding google geolocation response

        self.response = []
        self.payload = {}

        self.WifiObject = wifiScannerWindows.WifiGrab()  # to grab BSSIDs
        self.ssids, self.bssids, self.rssi, self.channel = self.WifiObject.all()

    def buildJSON(self, considerIP='true'):
        if len(self.bssids) < 3:
            print 'Atleast two BSSIDs are required.'
            print 'Current number of bssids: %i' % len(self.bssids)
            return

        # Building payload as per google-guidelines
        self.payload['considerIp'] = considerIP
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
            text = json.loads(self.response.text)

            if self.response.ok == False:  # Check if the response was ok
                if text['error']['errors'][0]['reason'] == 'dailyLimitExceeded':
                    print 'You have exceeded you daily limit'
                elif text['error']['errors'][0]['reason'] == 'keyInvalid':
                    print 'Your API key is not valid for the Google Maps Geolocation API'
                elif text['error']['errors'][0]['reason'] == 'userRateLimitExceeded':
                    print 'You\'ve exceeded the requests per second per user limit that you configured in the Google Developers Console'
                elif text['error']['errors'][0]['reason'] == 'notFound':
                    print 'The request was valid, but no results were returned'
                elif text['error']['errors'][0]['reason'] == 'parseError':
                    print 'The request body is not valid JSON'
                else:
                    print 'Unknown error in the geolocation response. Might be caught in an exception.'
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
        accuracy = response['accuracy']
        return lat, lng, accuracy

geolocateMe = geolocate(geolocateApiKey)    # replace geolocateApiKey variable at the top with your API key
geolocateMe.buildJSON(considerIP='true')    # build JSON request object
geolocateMe.request()                       # Send request to google
# geolocateMe.printResponse()               # Print response from google

# opening map
lat, lng, accuracy = geolocateMe.getLongLat()
mapObj = myMap.htmlMap(googlemapsApiKey, lat, lng, accuracy)
mapObj.createMap(map='yourLocation.html')
mapObj.openMap()

# Printing
lat, lng, accuracy = geolocateMe.getLongLat()
print 'Your geographic coordinates: '
print 'Latitude\t'+ str(lat)
print 'Longitude\t'+ str(lng)
print 'Accuracy\t' + str(accuracy) + 'm' + '\n\n'

# Using longitude and latitude information to print your address. The result will be formatted in several different ways
print 'Your physical address (formatted) is as follows:'
reverseGeocodeMe = ReverseGeocode(lat, lng, googlemapsApiKey)
reverseGeocodeMe.request()
reverseGeocodeMe.printResponse()