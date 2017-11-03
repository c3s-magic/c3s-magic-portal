#!/bin/bash
echo ADAGUC_SERVICES_HOME=${ADAGUC_SERVICES_HOME}

# Setup dirs
mkdir -p ${ADAGUC_SERVICES_HOME}/data/adaguc-services-base
mkdir -p ${ADAGUC_SERVICES_HOME}/data/adaguc-services-space
mkdir -p ${ADAGUC_SERVICES_HOME}/security
mkdir -p ${ADAGUC_SERVICES_HOME}/.globus/certificates
mkdir -p ${ADAGUC_SERVICES_HOME}/adaguc-services-tmp
mkdir -p ${ADAGUC_SERVICES_HOME}/wpsoutputs

### Setup truststore and keystore ###

# If needed create a self signed certificate in a keystore for serving over HTTPS
if [ ! -f ${ADAGUC_SERVICES_HOME}/security/keystore.jks ]; then
  keytool -genkey -noprompt -keypass password -alias tomcat \
  -keyalg RSA -storepass password -keystore ${ADAGUC_SERVICES_HOME}/security/keystore.jks -deststoretype pkcs12 \
  -dname CN=`hostname`
fi


# If needed create a truststore based on java truststore
if [ ! -f ${ADAGUC_SERVICES_HOME}/security/truststore.ts ]; then
  cp /usr/lib/jvm/java/jre/lib/security/cacerts ${ADAGUC_SERVICES_HOME}/security/truststore.ts
fi

### Make sure that this service trusts itself by adding its certificate to the trust store ###

# 1) Export certificate from a keystore to a file called adaguc-services-cert.pem
keytool -export -alias tomcat -rfc -file adaguc-services-cert.pem -keystore ${ADAGUC_SERVICES_HOME}/security/keystore.jks -storepass password

# 2) Put this certificate from adaguc-services-cert.pem into the truststore
keytool -delete -alias adagucservicescert -keystore ${ADAGUC_SERVICES_HOME}/security/truststore.ts -storepass changeit -noprompt
keytool -import -v -trustcacerts -alias adagucservicescert -file adaguc-services-cert.pem -keystore ${ADAGUC_SERVICES_HOME}/security/truststore.ts -storepass changeit -noprompt

### Make sure that this services trusts the controller(s) as well ###

# Create CA for tokenapi: file and key for  authority /O=KNMI/OU=RDWDT/CN=adaguc-services_ca_tokenapi"

if [ ! -f ${ADAGUC_SERVICES_HOME}/security/adaguc-services-ca.cert ]; then

openssl req \
    -new \
    -newkey rsa:4096 \
    -days 365 \
    -nodes \
    -x509 \
    -subj "/O=KNMI/OU=RDWDT/CN=adaguc-services_ca_tokenapi" \
    -keyout ${ADAGUC_SERVICES_HOME}/security/adaguc-services-ca.key \
    -out ${ADAGUC_SERVICES_HOME}/security/adaguc-services-ca.cert

# Put this CA in the truststore

keytool -delete -alias adaguc-services-ca -keystore ${ADAGUC_SERVICES_HOME}/security/truststore.ts -storepass changeit -noprompt
keytool -import -v -trustcacerts -alias adaguc-services-ca -file ${ADAGUC_SERVICES_HOME}/security/adaguc-services-ca.cert -keystore ${ADAGUC_SERVICES_HOME}/security/truststore.ts -storepass changeit -noprompt
else
  echo "Using CA file ${ADAGUC_SERVICES_HOME}/security/adaguc-services-ca.cert"
fi

HOME=$ADAGUC_SERVICES_HOME

echo "Starting POSTGRESQL DB" && \
runuser -l postgres -c "pg_ctl -w -D /postgresql -l /var/log/postgresql.log start" && \
mkdir -p /data/adaguc-autowms/ && \
mkdir -p /data/adaguc-datasets/ && \
cp /src/adaguc-server/data/datasets/testdata.nc /data/adaguc-autowms/ && \
cp /src/adaguc-server/data/config/datasets/dataset_a.xml /data/adaguc-datasets/ && \
echo "Configuring POSTGRESQL DB" && \
runuser -l postgres -c "createuser --superuser adaguc" && \
runuser -l postgres -c "psql postgres -c \"ALTER USER adaguc PASSWORD 'adaguc';\"" && \
runuser -l postgres -c "psql postgres -c \"CREATE DATABASE adaguc;\"" && \
echo "Starting TOMCAT Server" && \
java -jar /src/adaguc-services.war