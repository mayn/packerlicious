#!/bin/bash

LATEST_PACKER=`curl https://releases.hashicorp.com/packer/ | grep -Po 'packer_(\d+\.){2,3}\d+' | sort -V | tail -1`
set -- "$LATEST_PACKER"
IFS="_"; declare -a Elements=($*)
PACKER_VERSION="${Elements[1]}"
echo "Latest Packer version is ${PACKER_VERSION}"
wget --quiet "https://releases.hashicorp.com/packer/${PACKER_VERSION}/${LATEST_PACKER}_linux_amd64.zip"
unzip "${LATEST_PACKER}_linux_amd64.zip" -d ../