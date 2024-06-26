# Deployment of `labelstudio`
This section provides instructions to deploy `labelstudio` on a server. In many configurations a proxy server is used which proxies the requests to the services running in docker containers. The setup consists normally of setting up the proxy server (with https certificates) and the server with running the docker containers.

## Setup actual server
On the actual server the containers are orchestrated using `docker-compose`.

### Login to server
FIXME: ssh certificates not working for the jump to the individual nodes
FIXME: better storage handling
```
ssh denbi-node-6
```

### Clone repository
```bash
cd /var/git
git clone https://github.com/matthiaskoenig/labelstudio.git
cd labelstudio
mkdir data
chown 1000 data
```

### Start containers

```bash
git pull
# stop old containers
docker-compose -f docker-compose.yml down

# cleanup data
rm -rf data
mkdir data
sudo chown -R 1000:1000 data
sudo chmod -R 777 data

# allow login
LABEL_STUDIO_DISABLE_SIGNUP_WITHOUT_LINK=false

# start server
docker-compose -f docker-compose.yml up --detach

# create login
LABEL_STUDIO_DISABLE_SIGNUP_WITHOUT_LINK=true
docker-compose -f docker-compose.yml up --detach
```

### Test connection
Test that the service is running and can be reached
```bash
docker container ls
```
which should show the running container
```
CONTAINER ID   IMAGE                             COMMAND                  CREATED         STATUS                  PORTS                                       NAMES
135f09b49ab8   heartexlabs/label-studio:latest   "./deploy/docker-ent…"   4 seconds ago   Up Less than a second   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   labelstudio_labelstudio_1
```

```bash
curl localhost:8123/index.html
```

## Setup proxy server
The proxy server requires a proxy nginx configuration and the necessary certificates.
Login to proxy server `denbi-head`

### Configure domain
Define IP for domain or subdomain in strato.
Domains verwalten -> Eigene IP-Adresse: 134.176.27.178

### Certificates
Certificates are issued and renewed with letsencrypt.

#### Initial certificates
```bash
sudo mkdir -p /usr/share/nginx/letsencrypt
sudo service nginx stop
sudo certbot certonly -d annotatedb.com
sudo service nginx start
sudo service nginx status
```

#### Certificate renewal
```bash
sudo certbot certonly --webroot -w /usr/share/nginx/letsencrypt -d annotatedb.com --dry-run
```

### Activate page in nginx  
The page must be copied and activated. Make sure to **update the IP** of the server in nginx configuration!
```bash
cd /var/git
git clone https://github.com/matthiaskoenig/labelstudio.git
cd labelstudio

sudo cp /var/git/labelstudio/nginx/annotatedb.com /etc/nginx/sites-available/annotatedb.com
sudo ln -s /etc/nginx/sites-available/annotatedb.com /etc/nginx/sites-enabled/
sudo service nginx restart
sudo service nginx status
```
```bash
curl http://192.168.0.135:8123/index.html
```