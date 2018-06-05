#!/bin/bash -e 
function prompt_info() {
    echo -e "\033[0;32m[INFO]\033[0m $1"
}

function prompt_warn() {
    echo -e "\033[1;33m[WARN]\033[0m $1"
}

function prompt_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
}

function prompt_input() {
    echo -e -n "\033[1;36m!!!\033[0m $1: "
}

# Prompt info or error accoring the first argument, exit for non-zero status_code
# param1 status_code 0 as no error
# param2 msg to output
# param3 flag determine log msg as error or warn
function prompt() {
    if [ $1 == "0" ]; then
        prompt_info "$2"
    else
        if [ ! -z $3 ]; then
            prompt_warn "$2"
        else
            prompt_error "$2"
            exit $1
        fi
    fi
}