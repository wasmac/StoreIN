from Google import Create_Service
import pandas
import os, shutil
import pickle
import requests
import ast
from os import path

class GooglePhotos:
    
    API_NAME = 'photoslibrary'
    API_Version = 'v1'
    CLIENT_SECRET_FILE = 'client_secret_storein.com.json'
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary', 
              'https://www.googleapis.com/auth/photoslibrary.sharing']
    REQUEST_BODY = {'album': {'title': 'StoreIN',
                              'coverPhotoBaseUrl': 'https://cdn.pixabay.com/photo/2012/04/12/20/12/x-30465_960_720.png=w2048-h1024'}}
    
    def __init__(self):
        self.init_service()
        self.check_folders()
        
    def init_service(self):
        self.service = Create_Service(GooglePhotos.CLIENT_SECRET_FILE, 
                                      GooglePhotos.API_NAME,
                                      GooglePhotos.API_Version, 
                                      GooglePhotos.SCOPES)
    
    def list_api_folders(self):
        self.albums = self.service.albums().list(pageSize = 50,
                                         excludeNonAppCreatedData = True
                                         ).execute()
        albums_list = self.albums.get('albums')
        nextPageToken = self.albums.get('nextPageToken')
        while nextPageToken:
            self.albums = self.service.albums.list(pageSize=50,
                                   excludeNonAppCreatedData=True,
                                   pageToken=nextPageToken)
            albums_list.append(self.albums.get('ablums'))
            nextPageToken = self.albums.get('nextPageToken')
        df_albums = pandas.DataFrame(albums_list)
        return df_albums
    
    def check_folders(self):
        temp_list = self.list_api_folders()
        if not temp_list.empty:
            if temp_list['title'].any() == 'StoreIN':
                self.temp_copy = temp_list
                self.my_album_id = temp_list[temp_list['title']=='StoreIN']['id'][0]
            else:
                temp_body = self.service.albums().create(body = GooglePhotos.REQUEST_BODY).execute()
                enrichement_body = {'newEnrichmentItem':
                                    {'textEnrichment':
                                        {'text': 'This album contains the photos of valid receipts stored thanks to StoreIN app, please make sure to not change or delete anything while not using the app itself. Such behavior may create some issues while using the app. Thank you for cooperation.'}},
                                    'albumPosition': {'position': 'LAST_IN_ALBUM'}}
                self.service.albums().addEnrichment(albumId=temp_body.get('id'),
                                        body=enrichement_body).execute()
                self.my_album_id = temp_body.get('id')
        else:
            temp_body = self.service.albums().create(body = GooglePhotos.REQUEST_BODY).execute()
            enrichement_body = {'newEnrichmentItem':
                                {'textEnrichment':
                                    {'text': 'This album contains the photos of valid receipts stored thanks to StoreIN app. Please make sure to not change or delete anything while not using the app itself, such behavior may create some issues while using the app. Thank you for cooperation.'}},
                                'albumPosition': {'position': 'LAST_IN_ALBUM'}}
            self.service.albums().addEnrichment(albumId=temp_body.get('id'),
                                        body=enrichement_body).execute()
            self.my_album_id = temp_body.get('id')    
    
    def delete_empty_lines(self, my_file = "location_enrichments.txt"):
        with open(my_file,'r+') as file:
            for line in file:
                if not line.isspace():
                    file.write(line)
    
    def check_enrichments(self):
        dictionary = {}
        i = 1
        if not os.path.exists('location_enrichments.txt'):
            with open('location_enrichments.txt', 'w') as file:
                pass
            file.close()
        #self.delete_empty_lines()
        with open("location_enrichments.txt", "r") as file:
            lines = [line.rstrip() for line in file]
        file.close()
        for x in lines:
            temp = {}
            temp.update(ast.literal_eval(x))
            dictionary[i] = temp
            i = i+1
        return dictionary
   
    def check_if_location_already_exists(self, loc_name = " "):
        #self.delete_empty_lines()
        for line_number,line_content in self.check_enrichments().items():
            for key in line_content:
                if loc_name in line_content[key]:
                    if loc_name == line_content[key]:
                        return line_content["ID"]
                    else:
                        return False
    
    
    def add_location(self, lat = 0, lon = 0, loc_name = "None", **kwargs):
        temp = self.check_if_location_already_exists(loc_name = loc_name)
        print(temp)
        if temp is not None:
            return temp
        else:
            self.latitude = lat
            self.longitude = lon
            self.location_name = loc_name
            enrichement_body ={"newEnrichmentItem": {
                                "locationEnrichment": {
                                  "location": {
                                    "latlng": {
                                      "latitude": self.latitude,
                                      "longitude": self.longitude
                                    },
                                    "locationName": self.location_name
                                  }
                                }
                              },
                              "albumPosition": {
                                "position": "LAST_IN_ALBUM"
                              }
                            }
            response = self.service.albums().addEnrichment(albumId=self.my_album_id,
                                                body=enrichement_body).execute()
            f=open("location_enrichments.txt", "a+")
            f.write("{{'Name': '{}', 'latitude': '{}', 'longitude': '{}', 'ID': '{}'}}\r".format(self.location_name, self.latitude, self.longitude, response['enrichmentItem']['id']))
            f.close
            #self.delete_empty_lines()
            return response['enrichmentItem']['id']
    
    # create method in mainy.py that will check if user wants to add the location or not 
    #atm method takes values for only created enrichment
    def upload_image(self, file_name = 'dummy2.png', relativeEnrichmentItemId = None, posistion = "LAST_IN_ALBUM", uploaded_file_name = " ", **kwargs):
        #relativeEnrichmentItemId = self.check_enrichment()['ID']
        posistion = "AFTER_ENRICHMENT_ITEM"
        image_dir = os.path.join(os.getcwd(), 'imagestoupload')
        token = pickle.load(open('token_photoslibrary_v1.pickle', 'rb'))
        upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
        headers = {'Authorization': 'Bearer ' + token.token,
                   'Content-type': 'application/octet-stream',
                   'X-Goog-Upload-Protocol': 'raw',
                   'X-Goog-File-Name': file_name
                   }    
        image_file = os.path.join(image_dir, file_name)
        img = open(image_file, 'rb').read()
        response = requests.post(upload_url, data=img, headers=headers)        
        request_body = {"newMediaItems": [{"description": 'Name|Date|Years to expire',
                                           "simpleMediaItem": 
                                               {"fileName": uploaded_file_name,
                                                "uploadToken": response.content.decode('utf-8')
                                                }
                                               }
                                               ],
                                                "albumId": self.my_album_id,
                                                "albumPosition":
                                                    {"relativeEnrichmentItemId": relativeEnrichmentItemId,
                                                     "position": posistion
                                                     }
                                                    }
        
        self.service.mediaItems().batchCreate(body=request_body).execute()
        #print('\nUpload token: {0}'.format(response.content.decode('utf-8')))
        #return response
    
    
        
    def get_enrichment_id(self): #method to find enrichement ID for response body below
        print(self.add_location())
   
    def list_thumbnails(self):
        thumbnails = {}
        i = 0
        media_files = self.service.mediaItems().search(body={'albumId': self.my_album_id}).execute()['mediaItems']
        #print(media_files)
        for media_file in media_files:
            temp = {}
            temp.update({"file_name": media_file["filename"]})
            temp.update({"download_url": media_file["baseUrl"] + '=w128-h128'})
            thumbnails[i] = temp
            i = i+1
        return thumbnails
        #image = Image.open('image.jpg')
        #image.show()
    
    def download_file(self, url: str, file_name: str):
        response = requests.get(url)
        if response.status_code == 200:
            temp_name = file_name.split('|')[0] + '.png'
            if not os.path.exists(file_name + 'png'):
                # with open('tmp/' + temp_name, 'w') as file:
                #     file.close()
            #remember to add smth taht changes name if already exists
                with open('tmp/' + temp_name, 'wb') as file:
                    content = response.content
                    file.write(content)
                    file.close()
        else:
            return response.status_code
    
        #method for creating one pic
    def create_im(self):
        file_name = 'pieknyja|2020-05-01|2'
        url = self.list_thumbnails().get(10,'').get('download_url','')
        content = self.download_file(url, file_name)
        #print(content)
        temp_name = file_name.split('|')[0] + '.png'
        if not os.path.exists(file_name + 'png'):
            with open('tmp/' + temp_name, 'w') as file:
                file.close()
            with open('tmp/' + temp_name, 'wb') as file:
                file.write(content)
                file.close()
        else:
            pass
            
    
    def download_thumbnails(self, number_of_items_to_download: int):
        if number_of_items_to_download == -1:
            sliced_part = self.list_thumbnails()
        else:
            sliced_part = {k: self.list_thumbnails()[k] for k in sorted(self.list_thumbnails().keys())[:number_of_items_to_download]}
        for key in sliced_part:
            #print(key)
            url = sliced_part.get(key,'').get('download_url','')
            file_name = sliced_part.get(key,'').get('file_name','')
            if path.exists('tmp/' + file_name + '.png'):
                pass
            else:
                self.download_file(url, file_name)
        return number_of_items_to_download
            
    def delete_thumbnails(self):
        folder = 'tmp/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
            
            
        
    
    
    

if __name__ == '__main__':
    gp = GooglePhotos()
    #gp.download_thumbnails(5)
    gp.delete_thumbnails()
    #gp.create_im()
    #url = 'https://lh3.googleusercontent.com/lr/AFBm1_ZtG5b1WX30UZazbuVueigjgx-HiR-a5pzwP4rixJ16fWKE5dKKLPFX9Vlq8ev8tfqnYYHZJqOirRq_Eo0bzm6rIcmZHCFngvW9GEx0ODh9_IyTvS1JQO9xYn187CJIjqa63-6gXOl_dXYoOdQCZ57qsPnwjYaei9J8M1C27YCo-7bRkDl6dMKoJ8RPX4hKK0ArbQo0GrhgpAt2avOzEOOHpGwF1doi46OOlBXzfZWSfgZdHjyWgkWviRMeIQyLJqJpW7UyKQwoFjLhrqDsc8YKVA5cPCm1z1WOONCYO2KARU2Z61FEkZrSEQn0BRSb8Mz20an9NRnRK61LbE1NVzpSHKGkpLbbBhZDqwf27wvyN2vqG-p4usXHmpfX15-SOCK3e8fP0eAh9O9h2Q39182yGeJ0PpwVO83oxeJlWezd1s-fiLyz1mUMw-AgQWDlpZG87fyIgQDbecH5W1zSfyB3H2qj2qBsrdXIxg9q0cbiuuvJrd6utX2jKhm9o6AqmpTm2Esyl3lleeK1ztwwqofso8wtjdP-Rsk12JQMbgIapY15Dt-agqtnY58RyUi4SHs2BvAY70dyB1Q8ImKlVmNW9p8Qsj2lBN4mbuyIWh2YxMHSiaEPEzrWZY4Bu86TYtaluW9c5nTHkL85EUvXoI0nGqbqzc7xOh_84U7upUWuKoxfrsuxE-dkWqtQX00kZAMiJZ5-UJ6zn7Y2MjJUmK-Oy9CTJBPxYJ59oThH_VJFtvAQP17tiFgI17wr719btCrMEiZoNwwqQlYu70eMebBORGuPSF7fh6kyy6Kf9o03-sAJJ1LOSHvhrGsd=w128-h128'
    #file_name = 'pieknyja|2020-05-01|2'
    #gp.[10]['download_url']
    #print(gp.list_thumbnails())
    #print(gp.add_location(loc_name = "Makowa"))
    #print(gp.load_enrichmentID(loc_name = "Makowa"))
    #gp.upload_image()
    #print(gp.check_enrichments())
    #gp.get_enrichment_id()
    #
    #
    #print(gp.list_api_folders()['title'])
    #print(gp.check_folders())