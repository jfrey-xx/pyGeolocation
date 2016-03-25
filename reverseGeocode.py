import json
import requests


class ReverseGeocode:
    def __init__(self, lat, lng, geocodeApiKey):
        self.lat = str(lat)
        self.lng = str(lng)
        self.key = str(geocodeApiKey)

        self.response = []
        self.payload = {}

        self.headers = {
            'content-type': 'application/json',
        }

    def request(self):  # Send request to geolocate and return the response
        try:
            url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + self.lat + ',' + self.lng + '&key=' + self.key
            self.response = requests.post(url, headers=self.headers)
        except Exception, e:
            print str(e)

    def replaceKey(self, key):  # Replace geolocate API key
        self.key = key

    def printResponse(self):
        try:
            response = self.getResponse()
            for i in range(0,len(response['results'])):
                print response['results'][i]['formatted_address']
        except Exception, e:
            print str(e)

    def getResponse(self):
        return json.loads(self.response.text)


#rGeocode = ReverseGeocode('33.701282299999995', '72.9798076', geocodeApiKey)  # replace geocodeApiKey variable at the top with your API key
#rGeocode.request()    # Send request to google
#rGeocode.printResponse()  # Print response from google