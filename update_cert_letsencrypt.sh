#/bin/bash

COMPUTEHOME=adaguc-services-compute/adaguc-services-compute-home
CONTROLLERHOME=adaguc-services-controller/adaguc-services-controller-home
HOSTNAME=portal.c3s-magic.eu

#1 convert letsencrypt certificate to PKCS12 file
#  uses sudo to get to certificate in /etc/
sudo openssl pkcs12 -export -in /etc/letsencrypt/live/$HOSTNAME/fullchain.pem -inkey /etc/letsencrypt/live/$HOSTNAME/privkey.pem -out fullchain_and_key.p12 -name tomcat -passout pass:password

#1 remove old keystore
rm ${CONTROLLERHOME}/security/keystore.jks

#2 create new keystore containing certificate
keytool -importkeystore -deststorepass password -destkeystore ${CONTROLLERHOME}/security/keystore.jks -srckeystore fullchain_and_key.p12 -srcstoretype PKCS12 -srcstorepass password -alias tomcat

keytool -delete -alias letsencryptca -keystore ${CONTROLLERHOME}/security/truststore.ts -storepass changeit -noprompt
sudo keytool -import -v -trustcacerts -alias letsencryptca -file /etc/letsencrypt/live/$HOSTNAME/chain.pem -keystore ${CONTROLLERHOME}/security/truststore.ts -storepass changeit -noprompt

#also use keystore for compute container
cp ${CONTROLLERHOME}/security/keystore.jks ${COMPUTEHOME}/security/keystore.jks 
cp ${CONTROLLERHOME}/security/truststore.ts ${COMPUTEHOME}/security/truststore.ts 
