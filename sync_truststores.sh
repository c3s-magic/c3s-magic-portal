#/bin/bash

COMPUTEHOME=adaguc-services-compute-home
CONTROLLERHOME=adaguc-services-controller-home

# 1) Export certificate from remote keystore to a file called adaguc-compute-001.pem:
keytool -export -alias tomcat -rfc -file adaguc-compute-001.pem -keystore ${COMPUTEHOME}/security/keystore.jks -storepass password

# 2) Put this certificate from adaguc-compute-001.pem into controllers truststore
keytool -delete -alias adaguc-compute-001 -keystore ${CONTROLLERHOME}/security/truststore.ts -storepass changeit -noprompt
keytool -import -v -trustcacerts -alias adaguc-compute-001 -file adaguc-compute-001.pem -keystore ${CONTROLLERHOME}/security/truststore.ts -storepass changeit -noprompt

# 3) Export CA of this instance into truststore of remote instance
keytool -delete -alias controller-instance-001 -keystore ${COMPUTEHOME}/security/truststore.ts -storepass changeit -noprompt
keytool -import -v -trustcacerts -alias controller-instance-001 -file ${CONTROLLERHOME}/security/adaguc-services-ca.cert -keystore ${COMPUTEHOME}/security/truststore.ts -storepass changeit -noprompt
      
#Restart both dockers      