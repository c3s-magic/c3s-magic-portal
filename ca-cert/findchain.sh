#!/bin/bash
# Maarten Plieger, 2018-11-16
# This script composes from a set of certifificates, for given subject, a single bundle representing the certificate chain
# The bundle is useful for the nginx ssl_client_certificate setting

subjecttofind="DC=uk, DC=ac, DC=ceda, O=STFC RAL, CN=Centre for Environmental Data Analysis"

pushd /tmp/
curl -L https://raw.githubusercontent.com/ESGF/esgf-dist/master/installer/certs/esg_trusted_certificates.tar > esg_trusted_certificates.tar
tar -xvf esg_trusted_certificates.tar 
popd

certificatepath=/tmp/esg_trusted_certificates


echo "" > /tmp/bundle.pem
while true;do
  echo "Looking for subject [$subjecttofind]"
  # Loop through all certificates
  for file in $certificatepath/*.0;do 
    # Filter subject and issuer
    subject=`openssl x509 -in $file -text -noout | grep Subject`;
    cleansubject=${subject##*Subject:} && subject=`echo ${cleansubject%%Subject*} | sed 's/^ *//;s/ *$//'`
    issuer=`openssl x509 -in $file -text -noout | grep Issuer`;issuer=${issuer##*:}
    cleanissuer=${issuer##*Subject:} && issuer=`echo ${cleanissuer%%Subject*} | sed 's/^ *//;s/ *$//'`
    #Check if subject matches subject we are looking for
    a=`echo $subject | grep "$subjecttofind"`;
    if [[ ! -z "$a" ]]; then
      echo  ${file##*/}[$subject]"->"[$issuer]
      cat $file >> /tmp/bundle.pem
      if [ "$subjecttofind" == "$issuer" ]; then
        # Display bundle
        cat /tmp/bundle.pem
        exit
      fi
      subjecttofind="$issuer";      
    fi
  done
done
