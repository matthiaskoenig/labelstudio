# labelstudio

## Deployment of `labelstudio`
This section provides instructions to deploy `labelstudio` on a server. In many configurations a proxy server is used which proxies the requests to the services running in docker containers. The setup consists normally of setting up the proxy server (with https certificates) and the server with running the docker containers.

## Setup proxy server
The proxy server requires a proxy nginx configuration and the necessary certificates.
Login to proxy server `denbi-head`

### Activate page in nginx  
The page must be copied and activated. Make sure to **update the IP** of the server in nginx configuration!
```
cp <repo>/nginx/annotatedb.com /etc/nginx/sites-available/annotatedb.com
sudo ln -s /etc/nginx/sites-available/annotatedb.com /etc/nginx/sites-enabled/
```

### Certificates
Certificates are issued and renewed with letsencrypt.

#### Initial certificates
```
sudo mkdir -p /usr/share/nginx/letsencrypt
sudo service nginx stop
sudo certbot certonly -d annotatedb.com
sudo service nginx start
sudo service nginx status
```

#### Certificate renewal
```
sudo certbot certonly --webroot -w /usr/share/nginx/letsencrypt -d annotatedb.com --dry-run
```

## Setup actual server
On the actual server the containers are orchestrated using `docker-compose`.
Login to server `denbi-node-6`

### Clone repository
```
cd /var/git
git clone https://github.com/matthiaskoenig/labelstudio.git
cd labelstudio
mkdir data
```

### Start containers
```
git pull
docker-compose -f docker-compose.yml up --force-recreate --always-recreate-deps --build --detach
```

### Test connection
```
curl localhost:8123
```

# annotations
Label converter
https://github.com/HumanSignal/label-studio-converter

# Install with docker
https://labelstud.io/guide/install#Install-with-Docker

To install and start Label Studio at http://localhost:8080, storing all labeling data in ./mydata directory, run the following:
```
docker run -it -p 8080:8080 -v $(pwd)/mydata:/label-studio/data heartexlabs/label-studio:latest
```