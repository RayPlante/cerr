#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "${DIR}/.env"


echo "Tagging ${IMAGE_NAME}:${PROJECT_VERSION} as nistodi/cdcs_ce:${PROJECT_VERSION}"
docker tag ${IMAGE_NAME}:${PROJECT_VERSION} nistodi/cdcs_ce:${PROJECT_VERSION}

echo "Pushing nistodi/cdcs_ce:${PROJECT_VERSION} to Docker Hub"
docker push nistodi/cdcs_ce:${PROJECT_VERSION}
