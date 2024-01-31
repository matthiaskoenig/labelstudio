# Annotation formats
label-studio supports various annotation formats. A description of the available 
formats and how to export them is available here:

https://labelstud.io/guide/export#Label-Studio-JSON-format-of-annotated-tasks

## convert annotations
You can run the Label Studio converter tool on a directory or file of completed JSON 
annotations using the command line or Python to convert the completed annotations from 
Label Studio JSON format into another format.

https://github.com/heartexlabs/label-studio-converter
https://github.com/HumanSignal/label-studio-converter

# Installation
## Setup local server with docker
https://labelstud.io/guide/install#Install-with-Docker
To install and start Label Studio at http://localhost:8080, storing all labeling data in ./mydata directory, run the following:
```
docker run -it -p 8080:8080 -v ./data:/label-studio/data heartexlabs/label-studio:latest
```