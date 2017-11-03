
# docker build -t adaguc-services-compute .
# docker run -t adaguc-services-compute 
# docker run -e EXTERNALADDRESS="http://127.0.0.1:8080/" -p 8080:9000 -v $PWD/config:/config -v $PWD/adaguc-services-home/:/data/adaguc-services-home/ -it adaguc-services-compute /bin/bash

#https://localhost:8080/wms

#/data/adaguc-services-home

#docker exec -it  `docker ps -f ancestor=adaguc-services-compute -q` bash

#Processes can be places in
#/src/pywps/pywps/processes/



### Client: Make keypair and a certificate signing request###   

openssl genrsa -des3 -out clientkeywithpass.key 2048  -subj '/CN=testuser'  # Create user keypair
openssl rsa -in clientkeywithpass.key -out clientkey.key                    # Remove password
openssl req -new -key clientkey.key -out clientcsr.csr -subj '/CN=TESTER'   # Create Certificate Signing Request

### CA: Sign the CSR from the client. Normally the client sends his CSR to the CA which signs it and returns a certificate to the client ###
openssl x509 -req -in clientcsr.csr  -CA adaguc-services-home/security/adaguc-services-ca.cert -CAkey adaguc-services-home/security/adaguc-services-ca.key -CAcreateserial -out signedclientcert.crt -days 3600 #Sign CSR

### Client: Do a getuserinfofromcert request###
curl -k "https://localhost:7777/user/getuserinfofromcert" -v --key clientkey.key --cacert adaguc-services-ca.pem --cert signedclientcert.crt

### Client: Obtain an access token with the obtained client certificate by using the token api ###
curl -k "https://localhost:7777/registertoken" -v --key clientkey.key --cacert adaguc-services-ca.pem --cert signedclientcert.crt



