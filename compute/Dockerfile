FROM centos:7

MAINTAINER Adaguc Team at KNMI <adaguc@knmi.nl>

VOLUME /config
VOLUME /data

#TODO: perhaps host on a standard port (443)
EXPOSE 9000

# ImageMagick installed for cropping esmvaltool results in the wps process

RUN yum update -y && yum install -y \
    epel-release \
    netcdf-fortran-devel.x86_64\
    lapack-devel.x86_64 R\
    python-py\
    scipy\
    numpy\
    python-pandas\
    netcdf4-python\
    tomcat \
    openssl

RUN yum clean all && yum groupinstall -y "Development tools"

# Install adaguc-services from JITPACK
WORKDIR /src/adaguc-services
RUN curl -L https://jitpack.io/com/github/KNMI/adaguc-services/1.0.1/adaguc-services-1.0.1.war > /src/adaguc-services.war

# Install pywps
WORKDIR /src
RUN curl -L -O https://github.com/geopython/pywps/archive/pywps-3.2.5.tar.gz
RUN tar xvf pywps-3.2.5.tar.gz
RUN mv pywps-pywps-3.2.5 pywps

# Setup directories
WORKDIR /data/adaguc-services-home/

### CLIMATE EXPLORER section ###

RUN yum update -y && yum install -y \
    netcdf-fortran-devel.x86_64 \
    lapack-devel.x86_64 \
    R

WORKDIR /src
RUN git clone https://github.com/andrejsim/ClimExp-fortran.git
RUN mkdir -p ClimExp-fortran/build
# moved this library temporarily to git hub, can not locate relevant source online. (Pending)
RUN git clone https://github.com/andrejsim/nrf
RUN cd nrf && tar -xf nrf.tar && make -f nrf.mk && cd ..
RUN cp ./nrf/libnr.a ClimExp-fortran/build
COPY Makefile.docker ClimExp-fortran/build/Makefile
RUN cd ClimExp-fortran/build && make
ENV CLIMEXPFORTRAN=/src/ClimExp-fortran/build/

# Install wps_prov
WORKDIR /src
RUN git clone https://github.com/KNMI/wps_prov
WORKDIR /src/wps_prov
RUN python setup.py install

VOLUME /src/pywps/pywps/processes/
WORKDIR /src
RUN git clone https://github.com/maartenplieger/ClimExp-pyapi

WORKDIR /src/ClimExp-pyapi
RUN python setup.py install

ENV PYTHONPATH="/src/ClimExp-pyapi/wpsproc/prov:/src/wps_prov"

############### End of custom processes ###################


ENV ADAGUC_SERVICES_HOME=/data/adaguc-services-home/

# Configure adaguc-services
ENV ADAGUC_SERVICES_CONFIG=/config/adaguc-services-compute.xml

COPY ./start.sh /src/

RUN chmod +x /src/start.sh
ENTRYPOINT /src/start.sh

#docker build -t adaguc-services-compute .
#docker run -e EXTERNALADDRESS="http://127.0.0.1:8888/" -p 8888:9000 -v $PWD/config:/config -v $PWD/adaguc-services-home/:/data/adaguc-services-home/ -v $HOME/esmvaltool_input:/root/esmvaltool_input -v $HOME/esmvaltool_output:/root/esmvaltool_output -it adaguc-services-compute
#docker exec -it  `docker ps -f ancestor=adaguc-services-compute -q` bash

# PyWPS log: /data/adaguc-services-home/adaguc-services-tmp/pywps.log
