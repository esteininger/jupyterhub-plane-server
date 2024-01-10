1. clone plane `git clone https://github.com/drifting-in-space/plane.git` && `cd plane`
2. start plane: `docker compose -f docker/docker-compose.yml up`
3. create jupyterhub container: `docker build -t hub .`
4. run container in plane: 

```
docker/cli.sh \
    connect \
    --cluster 'localhost:9090' \
    --key 'my-first-backend' \
    --image 'ghcr.io/drifting-in-space/demo-image-drop-four' \
    --wait
```