from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
import time
from kivy.clock import Clock
from kivy.core.image import Image
import os
from googlephotos import GooglePhotos
import datetime
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
import os.path
import shutil
from infobanner import InfoBanner
from kivymd.toast import toast

class FirstLogScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class PictureScreen(Screen):
    pass

class SaveScreen(Screen):
    pass

class AlbumScreen(Screen):
    pass

class InfoScreen(Screen):
    pass

class ShopNameScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        self.root = Builder.load_file("main.kv")
        self.screen_manager = ScreenManager()
        self.screen_id = self.root.ids
        for k, v in self.screen_id.items():
            screen = Screen(name = k)
            self.screen_manager.add_widget(screen)
        self.google_connect() #for now in on_start() <- pos to be determined later
        self.camera_setup()
        return self.root
    
    def on_start(self):
        self.album_screen_elements = []
        self.populate_info_screen()
        self.populate_album_screen()
        self.drop_down_menu_init()
        #self.google_connect()
    
    def populate_info_screen(self):
        info_grid = self.root.ids['info_screen'].ids['info_grid']
        info_first = InfoBanner(description = "1. Make a photo",
                                image = "temp.png",
                                source = 'instruction/')
        info_secound = InfoBanner(description = "2. Select name and dates",
                                  image = "temp.png",
                                  source = 'instruction/')
        info_third = InfoBanner(description = "3. Scroll thorugh your valid receipts!",
                                image = "temp.png",
                                source = 'instruction/')
        info_grid.add_widget(info_first)
        info_grid.add_widget(info_secound)
        info_grid.add_widget(info_third)
    
    def populate_album_screen(self):
        #iterate thorugh all album/ folder objects
        #load first 20, if needed load next objects etc... 
        #put it in scrool view rows:3 cols:n 
        album_grid = self.root.ids['album_screen'].ids['album_grid']
        folder = 'tmp/'
        try:
            self.gp.download_thumbnails(-1)
          #  if [f for f in os.listdir('tmp/') if not f.startswith('.')] == []:
               # self.gp.download_thumbnails(-1)
           # else:
                #1: list files in StoreIN album
                #2: create list only with files that are not in temp folder
                #3: download missing files
            for file_name in os.listdir(folder):
                if file_name not in set(self.album_screen_elements):
                    temp_grid = InfoBanner(description =  file_name.split('.')[0],
                                        image = file_name,
                                        source = folder)
                    album_grid.add_widget(temp_grid)
                    self.album_screen_elements.append(file_name)
        except:
            toast('You dont have any receipts uploaded yet.')
                
    def update_album_screen(self): #-------------------tuuuuu
        pass
    
    def change_screen(self, screen_name):
        self.screen_manager.current(screen_name)
    
    def capture(self):
        camera = self.root.ids['home_screen'].ids['camera']
        timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = "IMG_" + timestr + ".png"
        self.im = Image(camera.texture)
        while not self.im.save(self.filename):
            time.sleep(0.001)
    
    def camera_setup(self):
        self.root.ids['home_screen'].ids['camera'].play = True
        
    def reload_picture(self):
        self.root.ids['picture_screen'].ids['picture'].picture_source = self.filename
    
    def remove_picture(self):
        os.remove(self.filename)
        
    def remove_pic_after_upload(self):
        os.remove("imagestoupload//{}".format(self.filename))
        
    def google_connect(self):
        self.gp = GooglePhotos()
        
    def debug_print(self):
        print(self.root.ids['picture_screen'].ids['picture'].picture_source)
  
    def show_date_picker(self, *args):
        self.date_picker = MDDatePicker(self.set_purchase_date)
        self.date_picker.open()
        
#    def show_date_picker(self):
#        date_picker = MDDatePicker(callback=self.get_date)
#        date_picker.open()
    
    def set_purchase_date(self, date_obj):
        self.purchase_date = date_obj
        self.root.ids['save_screen'].ids['date_picker_label'].text = str(date_obj)

    def get_receipt_name(self):
        receipt_name = str
        try:
            item_name = str(self.root.ids['save_screen'].ids['item_name'].text)                        
        except:
            item_name = "item"
        try:
            purchase_date = str(self.purchase_date)
        except:
            purchase_date = time.strftime("%Y-%m-%d")
        year_slider = str(round(self.root.ids['save_screen'].ids['year_slider'].value))
        receipt_name = (item_name + "|" + purchase_date + "|" + year_slider)
        
#        receipt_name = (str(self.root.ids['save_screen'].ids['item_name'].text) +
#                        "|" + str(self.purchase_date) + "|" +
#                        str(round(self.root.ids['save_screen'].ids['year_slider'].value)))
        return receipt_name
    
    def print_date_and_name(self):
#        try:
#            print(self.purchase_date) #date that was set by app user
#        except:
#            print(time.strftime("%Y-%m-%d"))
#        try:
#            print(self.root.ids['save_screen'].ids['item_name'].text) #name that was set by user
#        except:
#            self.root.ids['save_screen'].ids['item_name'].text = "item"
#            print(self.root.ids['save_screen'].ids['item_name'].text)
#        print(round(self.root.ids['save_screen'].ids['year_slider'].value)) # rounded val of slider
#        print("__________________")
        print(self.get_receipt_name())
        
#    def get_date(self):
#        todays_date = datetime.datetime.now()
#        print(todays_date.date())
#        return todays_date.date()

    def upload_complete(self):
        toast('Your receipt has been uploaded.')
        
        
    def load_shop_names(self):
        #shop_names = [{"icon": "git", "text": f"Item {i}"} for i in range(5)]
        shop_names = self.gp.check_enrichments()
        shop_names = [{"text": f"{shop_names[x]['Name']}"}for x in shop_names]
        return shop_names
    
    
    def drop_down_menu_init(self):
        menu_items = self.load_shop_names()
        self.menu = MDDropdownMenu(caller=self.root.ids['shop_name_screen'].ids['field'],
                                   items=menu_items,
                                   position="bottom",
                                   callback=self.set_item,
                                   width_mult=4,)
    
    def set_item(self, instance):
        def set_item(interval):
            #self.screen.ids.field.text = instance.text
            self.root.ids['shop_name_screen'].ids['field'].text = instance.text
        Clock.schedule_once(set_item, 0.1)
        
    def swap_image_dir(self):
        file = self.filename
        path = "imagestoupload"
        shutil.move(file, path)
    
    def upload_to_cloud(self):
        photo_name = self.filename
        uploaded_name = self.get_receipt_name()
        shop_name = self.root.ids['shop_name_screen'].ids['field'].text
        self.swap_image_dir()
        print("Photo is beeing uploaded")
        enrichmentID = self.gp.add_location(loc_name = shop_name)
        print("--------------------------------")
        self.gp.upload_image(file_name = photo_name,
                             relativeEnrichmentItemId = enrichmentID,
                             uploaded_file_name = uploaded_name)
        print("Receipt of: {} from: {} was uploaded".format(uploaded_name, shop_name))
        
    
MainApp().run()





############################# Function for hiding widgets
#    def hide_widget(wid, dohide=True):
#        if hasattr(wid, 'saved_attrs'):
#            if not dohide:
#                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
#                del wid.saved_attrs
#        elif dohide:
#            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
#            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True