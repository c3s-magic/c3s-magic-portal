FROM adaguc-services

# Setup directories
WORKDIR /data/adaguc-services-home/
ENV ADAGUC_SERVICES_HOME=/data/adaguc-services-home/

# Configure adaguc-services
ENV ADAGUC_SERVICES_CONFIG=/config/adaguc-services-compute.xml

# Copy processes
COPY ./processes/* /src/pywps/pywps/processes/

COPY ./start.sh /src/

RUN chmod +x /src/start.sh
ENTRYPOINT /src/start.sh

#docker build -t adaguc-services-compute .
#docker run -e EXTERNALADDRESS="http://127.0.0.1:8888/" -p 8888:9000 -v $PWD/config:/config -v $PWD/adaguc-services-home/:/data/adaguc-services-home/ -it adaguc-services-compute
#docker exec -it  `docker ps -f ancestor=adaguc-services-compute -q` bash