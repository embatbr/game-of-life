#!/bin/bash


export PROJECT_ROOT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd ${PROJECT_ROOT_PATH}


newborn=$1
keepalive=$2
input_name=$3


# python conway.py ${input_name}
python ${PROJECT_ROOT_PATH}/src/cellular_automatons.py ${newborn} ${keepalive} ${input_name}
