#!/usr/bin/env bash
source .env
echo "Add Users..."
#docker cp cdcs/$COMPOSE_PROJECT_NAME/$COMPOSE_PROJECT_NAME.json "cdcs_"$COMPOSE_PROJECT_NAME:/srv/curator/Users.json
docker cp Users.json "nmrr_cdcs":/srv/curator/Users.json
docker exec -u root "nmrr_cdcs" chown cdcs:cdcs Users.json
docker exec "nmrr_cdcs" python ./manage.py loaddata Users.json
