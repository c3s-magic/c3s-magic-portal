
# docker build -t adaguc-services-compute .
# docker run -t adaguc-services-compute 
# docker run -e EXTERNALADDRESS="http://127.0.0.1:8080/" -p 8080:9000 -v $PWD/config:/config -v $PWD/adaguc-services-home/:/data/adaguc-services-home/ -it adaguc-services-compute /bin/bash

#https://localhost:8080/wms

#/data/adaguc-services-home

#docker exec -it  `docker ps -f ancestor=adaguc-services-compute -q` bash

#Processes can be places in
#/src/pywps/pywps/processes/

#To setup a CA

### CA: Setup self signed CA ###
# Create private key for this certificate authority
openssl genrsa -out adaguc-services-ca.key 4096
# Create CA file for this authority
openssl req -x509 -days 3650 -new -nodes -key adaguc-services-ca.key -sha256 -out adaguc-services-ca.pem -subj '/O=KNMI/OU=RDWDT/CN=adaguc-services_ca_tokenapi'
# Put this CA in the truststore
sudo keytool -import -v -trustcacerts -alias adaguc-services-ca.pem -file adaguc-services-ca.pem -keystore ./adaguc-services-home/security/truststore.ts -storepass changeit -noprompt
# Restart the docker container.


### Client: Make keypair and a certificate signing request###   

openssl genrsa -des3 -out clientkeywithpass.key 2048  -subj '/CN=testuser'  # Create user keypair
openssl rsa -in clientkeywithpass.key -out clientkey.key                    # Remove password
openssl req -new -key clientkey.key -out clientcsr.csr -subj '/CN=TESTER'   # Create Certificate Signing Request

### CA: Sign the CSR from the client. Normally the client sends his CSR to the CA which signs it and returns a certificate to the client ###
openssl x509 -req -in clientcsr.csr  -CA adaguc-services-ca.pem  -CAkey adaguc-services-ca.key -CAcreateserial -out signedclientcert.crt -days 3600 #Sign CSR

### Client: Do a WPS GetCapabilities with the obtained client certificate ###
curl -k "https://localhost:8080/wps?request=getcapabilities&service=wps&version=1.0.0" -v --key clientkey.key --cacert adaguc-services-ca.pem --cert signedclientcert.crt

### Client: Obtain an access token with the obtained client certificate by using the token api ###
curl -k "https://localhost:8080/registertoken" -v --key clientkey.key --cacert adaguc-services-ca.pem --cert signedclientcert.crt

### Client: Do a WPS GetCapabilities with the obtained with the obtained key ###
curl -k "https://localhost:8080/wps?key=26875a22-3f30-4cd1-823d-a183484c3479&request=getcapabilities&service=wps&version=1.0.0"

### CLient: Execute WPS ###
curl -k "https://localhost:8080/wps?key=26875a22-3f30-4cd1-823d-a183484c3479&request=execute&identifier=binaryoperatorfornumbers_10sec&service=wps&version=1.0.0"
