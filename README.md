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


## Setup trainings database macrosteatosis
- copy images & raw predictions to folder and set the folder in the `.env` file
- update API key from labelstudio; https://annotatedb.com/user/account
- Create new project in labelstudio: `Macrosteatosis` and set value in `.env`
- Upload images to server; -> File Server: https://labelstud.io/guide/storage.html#Local-storage; mount volume in docker container; TODO: better solution for images; volume: `./data:/label-studio/data`
- scp -r steatosis_2024-03-05/ denbi-head:/home/ubuntu/
- scp -r steatosis_2024-03-05/ node6:/var/git/labelstudio/data/
- Settings -> Cloud Storage -> ... -> sync
- Setup labeling configuration; Settings -> Labeling Interface; 
```
<View>
  <Image name="image" value="$img"/>
	<KeyPointLabels name="keypoint" toName="image">
    <Label value="macrosteatosis keypoint" background="#04FF00"/>
  </KeyPointLabels>
  <BrushLabels name="brush" toName="image">
    <Label value="microsteatosis brush" background="#FFF79E"/>
  </BrushLabels>
  <PolygonLabels name="polygon" toName="image" strokeWidth="3" pointSize="small" opacity="0.3">
    <Label value="macrosteatosis polygon" background="#00FFFB"/>
  </PolygonLabels>
</View>
```
- run script
- run the `upload_prediction` script

## Annotation task
- open task
- settings: 
  - [x] show hotkeys on tooltips
- group by label, hide `polygon` to only see points
- annotate keypoints
  - select & move to center (dupletten; combined macrosteatosis droplets)
  - Select label at bottom (macrosteatosis keypoint 1) and click new
- to save click submit: can be changed later on
- objects for macrosteatosis should be larger then nucleus

## Export labels


Matthias König & Jonas Küttner 2024