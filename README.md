
## Deploying using docker-compose

 Add 127.0.1.1       portal.c3s-magic.eu to /etc/hosts    (portal.c3s-magic.eu is configured in console.developers.google.com for OAuth2 callback)
 Do docker-compose build --pull
 Do docker-compose up in working directory and go to localhost:80
 Do docker-compose down to stop all

#!/bin/bash 

docker exec c3s-magic-portal_backend_1 /adaguc/adaguc-server-updatedatasets.sh
