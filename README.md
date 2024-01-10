- clone plane `git clone https://github.com/drifting-in-space/plane.git` && `cd plane`
- start plane: `docker compose -f docker/docker-compose.yml up`
- create jupyterhub container: `docker build -t hub .`
- docker run -it --rm -p 8888:8888 hub
- run container in plane: 

```
docker/cli.sh \
    connect \
    --cluster 'localhost:9090' \
    --key 'my-first-backend' \
    --image 'ghcr.io/drifting-in-space/demo-image-drop-four' \
    --wait
```