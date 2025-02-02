#!/bin/bash


export PROJECT_ROOT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd ${PROJECT_ROOT_PATH}


class_path=$1
automaton_name=$2
input_name=$3


python ${PROJECT_ROOT_PATH}/src/main.py ${class_path} ${automaton_name} ${input_name}
