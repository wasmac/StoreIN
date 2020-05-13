# StoreIN
Python application that uses Kivy, KivyMD and GooglePhotos Api to help in receipt management.

## Files
Project files are divided into separate directories, one main (which contains all .py files alongside with main.kv file 
and directories like **imagestoupload**, **tmp**...) and directory named **kivy** that stores .kv files, 
which sotres files related to user interface.

## Requirements
### Python >=3.7 with libraries:
 - Kivy
 - KivyMD
 - google-api-python-client
 - google-auth-httplib2
 - google-auth-oauthlib
 - pickle
 - os
 - pandas
 - shutil
 - requests
 - ast
 
## Working principle
StoreIN asks user to provide the necessary permissions which allows the app to modify or create albums in users Google Photos service. (App can only modify files which was added/created by the app itself.)

<p align="center">
 <img width="400" height="460" src="https://github.com/wasmac/StoreIN/blob/master/images/1.PNG">
</p>

Application then goes to its default state, **homescreen** which is basicly an camera display.
<p align="center">
 <img width="300" height="460" src="https://github.com/wasmac/StoreIN/blob/master/images/2.PNG">
</p>
User then have various options like:

 - adding a new receipt
 - lookin up all added receipts
 - checking the information screen
 
 Adding a new receipt requires user to:

1) Make a photo,
2) Select name and dates of when item was bought and when receipt will expire,
3) Select shop name- from previously added ones or enter new shop name.
<p align="center">
 <img width="300" height="460" src="https://github.com/wasmac/StoreIN/blob/master/images/3.PNG">
</p>
After these easy steps the photo of receipt will be added to users cloud and stored within.

## Future development plans
 - once a week check if receipts are still valid, if no delete expired ones
 - optimize thumbnails algorithm
 - move application to iOS and Android platforms
>Application is under development.
