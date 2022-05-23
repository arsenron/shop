#!/bin/bash

docker-compose down --volumes  # start testing with fresh volume
docker-compose up -d
docker-compose run shop pytest
rc=$?
if [[ $rc != "0" ]]; then
  docker-compose logs | grep error
fi
docker-compose down --volumes
exit $rc
