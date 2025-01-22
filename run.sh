#!/bin/bash


export PROJECT_ROOT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd ${PROJECT_ROOT_PATH}


module=$1
automaton_name=$2
input_name=$3


# python conway.py ${input_name}
python ${PROJECT_ROOT_PATH}/src/${module}.py ${automaton_name} ${input_name}
