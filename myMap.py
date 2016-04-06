##############################################################
#
# Export an html file containing longitude and latitude to display
# in a google map
#
##############################################################
import webbrowser

class htmlMap():
    def __init__(self, key, lat, lng, accuracy):
        self.key = key
        self.lat = lat
        self.lng = lng
        self.accuracy = accuracy
        self.html = """<!DOCTYPE html>
    <html>
      <head>
        <title>Simple Map</title>
        <meta name="viewport" content="initial-scale=1.0">
        <meta charset="utf-8">
        <style>
          html, body {
            height: 100%;
            margin: 0;
            padding: 0;
          }
          #map {
            height: 100%;
          }
        </style>
      </head>
      <body>
        <div id="map"></div>
        <script>
          var map;
          function initMap() {
            map = new google.maps.Map(document.getElementById('map'), {
              center: {lat: """ + str(self.lat) + ', ' + 'lng: ' + str(self.lng) +'},' + """
              zoom: 18
            });

            var circle = new google.maps.Circle({
              strokeColor: '#FF0000',  // Color of the circle's outline
              strokeOpacity: 0.1,  // opacity of the circle
              strokeWeight: 1,  // defines the weight of the circle's outline
              fillColor: '#FF0000',  // color of the circle's fill
              fillOpacity: 0.20,  // defines the relative opacity
              map: map,
              center: {lat: """ + str(self.lat) + ', ' + 'lng: ' + str(self.lng) +'},' + """
              radius: """ + str(self.accuracy) + """  // standard unit is meters
            });
            var circle = new google.maps.Circle({
              strokeColor: '#000000',
              strokeOpacity: 1,
              strokeWeight: 2,
              fillColor: '#000000',
              fillOpacity: 1,
              map: map,
              center: {lat: """ + str(self.lat) + ', ' + 'lng: ' + str(self.lng) +'},' + """
              radius: 1
            });

            var infowindow = new google.maps.InfoWindow({
                content: 'lat: """ + str(self.lat) + ', ' + 'lng: ' + str(self.lng) + ', Accuracy: ' +  str(self.accuracy) + 'm' + """'
            });
            var marker = new google.maps.Marker({
              position: {lat: """ + str(self.lat) + ', ' + 'lng: ' + str(self.lng) +'},' + """
              map: map,
              title: 'Your Location!'
            });
            marker.addListener('click', function() {
                infowindow.open(map, this);
            });
          }
        </script>
        <script src="https://maps.googleapis.com/maps/api/js?key=""" + self.key + """&callback=initMap" async defer></script>
      </body>
    </html>"""

    def createMap(self, map='yourLocation.html'):
        f = open(map, 'w+')
        f.write(self.html)
        f.close()

    def openMap(self):
        webbrowser.open_new_tab('yourLocation.html')
