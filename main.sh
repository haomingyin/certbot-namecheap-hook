#!/bin/bash -e

# Required environment variables
# export API_USER=haomingyin
# export API_KEY=xxx
# export USERNAME=haomingyin
# export CLIENT_IP=127.0.0.1
# export SLD=haomingyin
# export TLD=com
# export APPLY_DOMAIN=*.haomingyin.com

# if CLIENT_IP is not set, then local IP will be used
if [ -z "$CLIENT_IP" ]; then
    localIp=$IP && [[ -z $IP ]] && localIp="$(dig +short myip.opendns.com @resolver1.opendns.com)"
    export CLIENT_IP=localIp
fi

# certbot renew \
# --logs-dir /usr/local/var/log/letsencrypt \
# --work-dir /usr/local/var/letsencrypt \
# --config-dir /usr/local/etc/letsencrypt \
# --preferred-challenges=dns \
# --pre-hook ./authenticator.sh \
# --post-hook ./cleanup.sh \
# --server https://acme-v02.api.letsencrypt.org/directory


certbot certonly \
--manual \
--logs-dir /usr/local/var/log/letsencrypt \
--work-dir /usr/local/var/letsencrypt \
--config-dir /usr/local/etc/letsencrypt \
--preferred-challenges=dns \
--manual-auth-hook ./authenticator.sh \
--manual-cleanup-hook ./cleanup.sh \
-d $APPLY_DOMAIN \
--server https://acme-v02.api.letsencrypt.org/directory \
--manual-public-ip-logging-ok \
--force-renewal
