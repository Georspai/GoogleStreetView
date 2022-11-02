#Version 4 of script to scrape Google Street View for 360 panoramas


import requests
import itertools
import shutil
import time
import cv2 
import numpy as np
from io import BytesIO
from os import getcwd,mkdir


def removeBlacktiles(img):
    
    # Convert RGB to BGR 
    #img = img[:, :, ::-1].copy() 
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)

    #find contours in it. There will be only one object, so find bounding rectangle for it.
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)

    #crop the image
    crop = img[y:y+h,x:x+w]

    return crop
    

class Panorama:
    def __init__(self,latitude,longitude,api_key):
        
        self.lat=latitude
        self.lng=longitude
        self._api_key=api_key
        self.status ,self.panoid , self.cam_lat , self.cam_lng=self.get_metadata()
        self.img=np.zeros((1000,1000))
        
        
        
    
    def get_metadataUrl(self):
    
        url="https://maps.googleapis.com/maps/api/streetview/metadata?location={},{}&key={}"
        return url.format(self.lat,self.lng,self._api_key)
    
    def _pano_metadata_request(self):
    
        url=self.get_metadataUrl()
        return requests.get(url,proxies=None)
    
    def get_metadata(self):

        resp=self._pano_metadata_request()
        if resp.status_code==200:
            status=resp.json().get("status")
            if resp.json().get("status")=='OK':
                
                panoid=resp.json().get("pano_id")
                cam_lat=resp.json().get("location").get("lat")
                cam_lng=resp.json().get("location").get("lng")
            else:
                panoid="None"
                cam_lat="None"
                cam_lng="None"
        else:
            print("gsv3.py\nResponse Return Error Code: "+ str(resp.status_code))
        del resp
        return status, panoid, cam_lat ,cam_lng

    def _tiles_info(self,zoom=4,nbt=0,fover=2):
        """
        Generate a list of a panorama's tiles and their position.
        The format is (x, y, filename, fileurl)
        """
        #Old url : image_url = 'http://maps.google.com/cbk?output=tile&panoid={}&zoom={}&x={}&y={}'
        image_url = "https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid={}&x={}&y={}&zoom={}&nbt={}&fover={}"

        # The tiles positions
        coord = list(itertools.product(range(2**zoom), range(2**(zoom-1))))
    
        tiles = [(x, y, "%s_%dx%d.jpg" % (self.panoid, x, y), image_url.format(self.panoid,x, y, zoom, nbt, fover)) for x, y in coord]
        return tiles

    def download_panorama(self,zoom=4):
    
        #Size of each tile that makes the panorama (subject to change)
        if zoom==5:
            tile_width = 256
            tile_height = 256
        else:
            tile_width = 512
            tile_height = 512

        # https://developers.google.com/maps/documentation/javascript/streetview#CreatingPanoramas
        img_w, img_h = 512*(2**zoom), 512*( 2**(zoom-1) )
        panorama= np.zeros(shape=[img_h, img_w, 3], dtype=np.uint8)

        tiles=self._tiles_info(zoom=zoom)
        valid_tiles=[]
        for x,y,fname,url in tiles:
            if x*tile_width < img_w and y*tile_height < img_h: # tile is valid
                # Try to download the image file
                while True:
                    try:
                        #print(url)
                        response = requests.get(url, stream=True)
                        break
                    except requests.ConnectionError:
                        print("Connection error. Trying again in 2 seconds.")
                        time.sleep(2)
                #print(response.json())
                #img=Image.open(BytesIO(response.content))
                #panorama.paste(im=img,box=(x*tile_width, y*tile_height))
                img=cv2.imdecode(np.frombuffer(BytesIO(response.content).read(), np.uint8), 1)
                try:
                    panorama[y*img.shape[1]:(y+1)*img.shape[1],x*img.shape[0]:(x+1)*img.shape[0],:]=img
                except:
                    print("Stitching error. Trying again.")
                del response

        self.img=panorama
        

    def save(self,directory,fname=None,extension='jpg', rmvbt=True):
        
       
        self.img=removeBlacktiles(self.img)
        

        
        if not fname:
            fname = "pano_%s" % (self.panoid)
        else:
            fname , ext =fname.split(".",1) 
        image_format = extension if extension != 'jpg' else 'jpeg'    
        try:
                filename="%s/%s.%s" % (directory,fname, extension)
                cv2.imwrite(filename,self.img)      
        except:
                print("Image not saved")



if __name__=="__main__" :
    #Latitude
    lat='13.512'
    #Longitude
    lng='55.729'
    #Google API key
    my_key=''

    dir='Panorama_test'
    
    newPano=Panorama(latitude=str(lat), longitude=str(lng) ,api_key=my_key)
    newPano.download_panorama(zoom=4)
    ff="pano_"+str(newPano.panoid)+".jpg"
    newPano.save(directory=dir,fname=ff)
