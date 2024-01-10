1. start plane: `docker compose -f docker/docker-compose.yml up`
2. create jupyterhub container: `docker build -t hub .`
3. run container in plane: 

```
docker/cli.sh \
    connect \
    --cluster 'localhost:9090' \
    --key 'my-first-backend' \
    --image 'ghcr.io/drifting-in-space/demo-image-drop-four' \
    --wait
```