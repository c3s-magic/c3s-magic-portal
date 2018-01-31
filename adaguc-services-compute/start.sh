#!/bin/bash

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

# 3) keytool -import -v -trustcacerts -alias controller-instance-001 -file ~/adaguc-services-controller-ws/security/adaguc-services-ca.pem -keystore ~/adaguc-services-compute-ws/security/truststore.ts -storepass changeit -noprompt


#

HOME=$ADAGUC_SERVICES_HOME

echo "Activating conda env"
source activate esmvalcondaenv


echo "Starting TOMCAT Server" && \
java -jar /src/adaguc-services.war