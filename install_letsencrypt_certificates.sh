#/bin/bash

SECURITY_COMPUTE=adaguc-services-compute/security
SECURITY_CONTROLLER=adaguc-services-controller/security

HOSTNAME=portal.c3s-magic.eu

echo ... convert letsencrypt certificate to PKCS12 file
#  uses sudo to get to certificate in /etc/
rm -f fullchain_and_key.p12
openssl pkcs12 -export -in /etc/letsencrypt/live/$HOSTNAME/fullchain.pem -inkey /etc/letsencrypt/live/$HOSTNAME/privkey.pem -out fullchain_and_key.p12 -name tomcat -passout pass:password

echo ... remove old keystore
rm -f ${SECURITY_CONTROLLER}/keystore.jks

echo ... create new keystore containing certificate
keytool -importkeystore -deststorepass password -destkeystore ${SECURITY_CONTROLLER}/keystore.jks -srckeystore fullchain_and_key.p12 -srcstoretype PKCS12 -srcstorepass password -alias tomcat

#remove temp key file
rm -f fullchain_and_key.p12

keytool -delete -alias letsencryptca -keystore ${SECURITY_CONTROLLER}/truststore.ts -storepass changeit -noprompt
keytool -import -v -trustcacerts -alias letsencryptca -file /etc/letsencrypt/live/$HOSTNAME/chain.pem -keystore ${SECURITY_CONTROLLER}/truststore.ts -storepass changeit -noprompt

echo ... also use keystore for compute container
cp ${SECURITY_CONTROLLER}/keystore.jks ${SECURITY_COMPUTE}/keystore.jks 
cp ${SECURITY_CONTROLLER}/truststore.ts ${SECURITY_COMPUTE}/truststore.ts 


