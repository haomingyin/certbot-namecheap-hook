#!/usr/bin/env bash

# Required environment variables
# export API_USER=usernmae
# export API_KEY=xxx
# export USERNAME=username
# export CLIENT_IP=127.0.0.1
export ACME_MODE=prod
# export EMAIL=email@gmail.com

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

# ----------------- certbot renew a wildcard cert --------------------
# certbot renew \
# --logs-dir /usr/local/var/log/letsencrypt \
# --work-dir /usr/local/var/letsencrypt \
# --config-dir /usr/local/etc/letsencrypt \
# --preferred-challenges=dns \
# --pre-hook ./authenticator.sh \
# --post-hook ./cleanup.sh \
# --server $ACME_SERVER
# ----------------------------------------------------------------------

# ---------- certbot certonly obtaining a new wildcard cert ------------
# certbot certonly \
# --manual \
# --logs-dir /usr/local/var/log/letsencrypt \
# --work-dir /usr/local/var/letsencrypt \
# --config-dir /usr/local/etc/letsencrypt \
# --preferred-challenges=dns \
# --manual-auth-hook ./authenticator.sh \
# --manual-cleanup-hook ./cleanup.sh \
# -d $APPLY_DOMAIN \
# -m $EMAIL \
# --server $ACME_SERVER \
# -agree-tos \
# --manual-public-ip-logging-ok \
# --force-renewal
# ----------------------------------------------------------------------

certbot renew \
  --preferred-challenges=dns \
  --manual-auth-hook ./authenticator.sh \
  --manual-cleanup-hook ./cleanup.sh \
  --server "$ACME_SERVER"
