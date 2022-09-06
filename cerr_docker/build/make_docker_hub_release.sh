#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "${DIR}/.env"


echo "Tagging ce:${PROJECT_VERSION} as nistodi/cdcs_ce:${PROJECT_VERSION}"
docker tag ce:${PROJECT_VERSION} nistodi/cdcs_cer:${PROJECT_VERSION}

echo "Pushing nistodi/cdcs_ce:${PROJECT_VERSION} to Docker Hub"
docker push nistodi/cdcs_ce:${PROJECT_VERSION}
