#/bin/bash

keytool -import -alias ceda -file /tmp/bundle.pem -keystore ../compute/security/truststore.ts -storepass changeit -noprompt
