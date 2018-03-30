#/bin/bash

# This script ensures that the controller and the compute instance are able to communicate with each other.

SECURITY_COMPUTE=adaguc-services-compute/security
SECURITY_CONTROLLER=adaguc-services-controller/security

# 1) Export certificate from remote keystore to a file called adaguc-compute-001.pem:
keytool -export -alias tomcat -rfc -file adaguc-compute-001.pem -keystore ${SECURITY_COMPUTE}/keystore.jks -storepass password

# 2) Put this certificate from adaguc-compute-001.pem into controllers truststore
keytool -delete -alias adaguc-compute-001 -keystore ${SECURITY_CONTROLLER}/truststore.ts -storepass changeit -noprompt
keytool -import -v -trustcacerts -alias adaguc-compute-001 -file adaguc-compute-001.pem -keystore ${SECURITY_CONTROLLER}/truststore.ts -storepass changeit -noprompt

# 3) Export CA of this instance into truststore of remote instance
keytool -delete -alias controller-instance-001 -keystore ${SECURITY_COMPUTE}/truststore.ts -storepass changeit -noprompt
keytool -import -v -trustcacerts -alias controller-instance-001 -file ${SECURITY_CONTROLLER}/adaguc-services-ca.cert -keystore ${SECURITY_COMPUTE}/truststore.ts -storepass changeit -noprompt
      
#Restart both dockers      