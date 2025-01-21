#!/bin/bash


export PROJECT_ROOT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd ${PROJECT_ROOT_PATH}


automaton_name=$1
input_name=$2


# python conway.py ${input_name}
python ${PROJECT_ROOT_PATH}/src/lifelike.py ${automaton_name} ${input_name}
