#!/usr/bin/env bash

# Required environment variables
# export API_USER=usernmae
# export API_KEY=xxx
# export USERNAME=username
# export CLIENT_IP=127.0.0.1
export ACME_MODE=prod

## Redirect back into the correct folder
SUB_DIR="$(dirname $0)"
if [[ "$PWD" != "$SUB_DIR" ]]; then
  cd "$SUB_DIR"
fi

# if CLIENT_IP is not set, then local IP will be used
. ./utility.sh
check_python_version
get_client_ip
get_acme_server

# Default dirs are not using because of the permission restriction on Mac OS

# --------------------- certbot renew all certs ------------------------
certbot renew \
  --preferred-challenges=dns \
  --manual-auth-hook ./authenticator.sh \
  --manual-cleanup-hook ./cleanup.sh \
  --server "$ACME_SERVER"
# ----------------------------------------------------------------------

# ---------- certbot certonly obtaining a new cert ------------
# export DOMAIN_NAME=example.com
# export EMAIL=email@gmail.com
# certbot certonly \
# --manual \
# --preferred-challenges=dns \
# --manual-auth-hook ./authenticator.sh \
# --manual-cleanup-hook ./cleanup.sh \
# --server $ACME_SERVER \
# -d $DOMAIN_NAME \
# -d "*.$DOMAIN_NAME" \
# -m $EMAIL \
# -agree-tos
# ----------------------------------------------------------------------
