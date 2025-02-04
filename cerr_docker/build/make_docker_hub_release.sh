#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "${DIR}/.env"


echo "Tagging ${IMAGE_NAME}:${IMAGE_VERSION} as nistodi/cdcs_ce:${IMAGE_VERSION}"
docker tag ${IMAGE_NAME}:${IMAGE_VERSION} nistodi/cdcs_ce:${IMAGE_VERSION}

echo "Pushing nistodi/cdcs_ce:${IMAGE_VERSION} to Docker Hub"
docker push nistodi/cdcs_ce:${IMAGE_VERSION}
