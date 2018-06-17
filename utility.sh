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

function _check_python_version() {
    if [ -x "$(command -v $1)" ]; then
        version=$($1 -V 2>&1 | awk '{print $2}' | awk -F '.' '{print $1}')
        if [ "$version" == '3' ]; then
            return 0
        fi
    fi
    return 1
}

# Python 3 is required to run the script
function check_python_version() {
    if _check_python_version python; then
        export PYTHON=python
    else
        if _check_python_version python3; then
            export PYTHON=python3
        else
            prompt_error "Python is not installed"
            exit 1
        fi
    fi
}

function get_client_ip() {
    if [ -z "$CLIENT_IP" ]; then
        localIp="$(dig +short myip.opendns.com @resolver1.opendns.com)"
        export CLIENT_IP=$localIp
    fi
    echo $CLIENT_IP
}

function get_acme_server() {
    if [ "$ACME_MODE" == "prod" ]; then
        export ACME_SERVER="https://acme-v02.api.letsencrypt.org/directory"
    else
        export ACME_SERVER="https://acme-staging-v02.api.letsencrypt.org/directory"
    fi
    echo $ACME_SERVER
}

# '$@' enables to call functions in utility.sh. Just use as
# $ ./utility.sh get_client_ip
# > 127.0.0.1
"$@"
