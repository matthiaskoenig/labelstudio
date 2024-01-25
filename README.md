# labelstudio

Setting up labelstudio server

![https://docs.heartex.com/images/LSE_k8s_scheme.png](https://docs.heartex.com/images/LSE_k8s_scheme.png)


# annotations
Label converter
https://github.com/HumanSignal/label-studio-converter

# Install with docker
https://labelstud.io/guide/install#Install-with-Docker

To install and start Label Studio at http://localhost:8080, storing all labeling data in ./mydata directory, run the following:
```
docker run -it -p 8080:8080 -v ./data:/label-studio/data heartexlabs/label-studio:latest
```