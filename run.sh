#!/bin/bash


export PROJECT_ROOT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd ${PROJECT_ROOT_PATH}


automaton_type=$1
input_name=$2


# python conway.py ${input_name}
python ${PROJECT_ROOT_PATH}/src/cellular_automatons.py ${automaton_type} ${input_name}
