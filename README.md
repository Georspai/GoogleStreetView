# GoogleStreetView

Python module to download 360 degree Panoramas from Google's Street View Platform.

A Google Maps API Key is needed in order to use the module.


Search street view for closest panorama to latitude and longitude 46.414382,10.013988:
Creates an Object with the metadata of said Panorama
- Latitude (.lat)
- Longitude (.lng)
- Google Maps API Key (.api_key)
- Status
- Panorama ID (.panoid)
- Camera Latitude (.cam_lat)
- Camera Longitude (.cam_lng)
- Panorama (.img) (Empty at first)

```newPano=Panorama(latitude='46.414382', longitude='10.013988' ,api_key='my_key')```

Download
