FROM c3smagic/adaguc-services

# Setup directories
WORKDIR /data/adaguc-services-home/

# Install climate explorer 
RUN yum update -y && yum install -y \
  netcdf-fortran-devel.x86_64\
  lapack-devel.x86_64 R\
  python-py\
  scipy\
  numpy\
  python-pandas\
  netcdf4-python 
  
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
RUN cd wps_prov && python setup.py install

VOLUME /src/pywps/pywps/processes/
#  Install climexp WPS
WORKDIR /src
RUN git clone https://github.com/maartenplieger/ClimExp-pyapi

RUN cd ClimExp-pyapi && python setup.py install
ENV PYTHONPATH="/src/ClimExp-pyapi/wpsproc/prov:/src/wps_prov"

ENV ADAGUC_SERVICES_HOME=/data/adaguc-services-home/

# Configure adaguc-services
ENV ADAGUC_SERVICES_CONFIG=/config/adaguc-services-compute.xml

COPY ./start.sh /src/

RUN chmod +x /src/start.sh
ENTRYPOINT /src/start.sh

#docker build -t adaguc-services-compute .
#docker run -e EXTERNALADDRESS="http://127.0.0.1:8888/" -p 8888:9000 -v $PWD/config:/config -v $PWD/adaguc-services-home/:/data/adaguc-services-home/ -it adaguc-services-compute
#docker exec -it  `docker ps -f ancestor=adaguc-services-compute -q` bash

# PyWPS log: /data/adaguc-services-home/adaguc-services-tmp/pywps.log