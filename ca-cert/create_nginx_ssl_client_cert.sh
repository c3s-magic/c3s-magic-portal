#/bin/bash
bash findchain.sh > /dev/null
cat ../backend/security/adaguc-services-ca.cert > nginx_ssl_client_certificate.pem
cat /tmp/bundle.pem >> nginx_ssl_client_certificate.pem
cat nginx_ssl_client_certificate.pem