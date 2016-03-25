<h1>pyGeolocation</h1>
Objective of this project is to create a script which can return longitude and latitude information of the client machine by utilizing wifi-geolocation API of Google.

Specific tasks:
1- Grab wifi names, mac addresses, signal strength and other relevant information (Ongoing)
2- Create a JSON request from this information and send to google for geolocation (Ongoing)
3- Use the longitude and latitude response to show a map snippet or physical address in text

As of 13-March-16, the script can grab BSSIDs from your vicinity, creates a JSON request and print the response.

<h2>USAGE</h2>
python geolocate.py <i>GEOLOCATION-API-KEY GEOCODE-API-KEY</i>
python geolocate.py -h
