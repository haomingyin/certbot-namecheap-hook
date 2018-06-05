# Manual Cleanup Hook

# Certbot will pass following environment variables to the script
# CERTBOT_DOMAIN: The domain being authenticated
# CERTBOT_VALIDATION: The validation string (HTTP-01 and DNS-01 only)
# CERTBOT_TOKEN: Resource name part of the HTTP-01 challenge (HTTP-01 only)
# CERTBOT_CERT_PATH: The challenge SSL certificate (TLS-SNI-01 only)
# CERTBOT_KEY_PATH: The private key associated with the aforementioned SSL certificate (TLS-SNI-01 only)
# CERTBOT_SNI_DOMAIN: The SNI name for which the ACME server expects to be presented the self-signed certificate located at $CERTBOT_CERT_PATH (TLS-SNI-01 only) 

# Additionally for cleanup:
# CERTBOT_AUTH_OUTPUT: Whatever the auth script wrote to stdout

