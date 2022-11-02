# GoogleStreetView

Python module to download 360 degree Panoramas from Google's Street View Platform.

A Google Maps API Key is needed in order to use the module.


Search street view for closest panorama to latitude and longitude 46.414382,10.013988: \
Creates an Object with the metadata of said Panorama


`` newPano=Panorama(latitude='13.18181649', longitude='55.70879272' ,api_key='my_key') ``

- Latitude (.lat)
- Longitude (.lng)
- Google Maps API Key (.api_key)
- Status
- Panorama ID (.panoid)
- Camera Latitude (.cam_lat)
- Camera Longitude (.cam_lng)
- Panorama (.img) (Empty at first)\


To Download the Panorama:

`` newPano.download_panorama(zoom=4) ``

Zoom parameter goes from 0 to 5

To save the Panorama:

`` newPano.save(directory='Path_to_dir,fname='filename') ``

### Example Output:
![test panorama]("https://github.com/Georspai/GoogleStreetView/blob/main/img/pano_test.jpg")
