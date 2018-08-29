FROM c3smagic/adaguc-services

# Setup directories
WORKDIR /data/adaguc-services-home/
ENV ADAGUC_SERVICES_HOME=/data/adaguc-services-home/

# Configure adaguc-services
ENV ADAGUC_SERVICES_CONFIG=/config/adaguc-services-controller.xml

COPY ./start.sh /src/
RUN chmod +x /src/start.sh
ENTRYPOINT /src/start.sh

#docker build -t adaguc-services-controller .
#docker run -e EXTERNALADDRESS="https://compute-test.c3s-magic.eu:7777" -p 7777:9000 -v $PWD/config:/config -v $PWD/adaguc-services-home/:/data/adaguc-services-home/ -it adaguc-services-controller
#docker exec -it  `docker ps -f ancestor=adaguc-services-controller -q` bash
#/data/adaguc-services-home//security/adaguc-services-ca.cert
