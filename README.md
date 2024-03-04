# label-studio-tools

This repository provides an interface for label-studio to programatically 
manage annotation tasks. Main focus is the annotation of histological images.

This uses the label-studio SDK to manage the annotation tasks.

https://labelstud.io/blog/5-tips-and-tricks-for-label-studio-s-api-and-sdk/  
https://labelstud.io/guide/sdk

# Installation
## virtual environment
Create a virtual environment and install the dependencies:

```bash
mkvirtualenv labelstudio --python=python3.11
(labelstudio) pip install -r requirements.txt
```

## SDK url and key
Create an `.env` file and add the `API_URL` and `API_KEY`.
The `API_KEY` is available from the label-studio interface under user settings.
```
cp .env.template .env
```

## Test connection
To test the SDK connection use the `sdktest.py` script.


## Setup trainings database
- copy images & raw predictions to folder and set the folder in the `.env` file
- update API key from labelstudio; https://annotatedb.com/user/account
- Create new project in labelstudio: `Macrosteatosis` and set value in `.env`
- Upload images to server; -> File Server: https://labelstud.io/guide/storage.html#Local-storage



- run the `upload_prediction` script


Matthias König & Jonas Küttner 2024