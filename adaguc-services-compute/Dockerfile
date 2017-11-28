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
  netcdf4-python\
  ImageMagick\
  && yum groupinstall -y "Development tools"

# install conda
WORKDIR /src
RUN curl -L -O https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
RUN bash ./Miniconda2-latest-Linux-x86_64.sh -p /miniconda -b
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda
RUN conda update -y pip

# ESMVALTOOL section

# get esmvaltool
WORKDIR /src
RUN git clone https://github.com/c3s-magic/ESMValTool
WORKDIR /src/ESMValTool
RUN git checkout REFACTORING_backend_perfmetrics_demo

# install esmvaltool
RUN conda env update --name root
# workaround: ncl install from conda is broken, see https://github.com/conda-forge/ncl-feedstock/issues/25
RUN conda install -y -c conda-forge poppler=0.52.0 xerces-c=3.1.4
RUN python setup.py install

# CLIMATE EXPLORER section

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
#docker run -e EXTERNALADDRESS="http://127.0.0.1:8888/" -p 8888:9000 -v $PWD/config:/config -v $PWD/adaguc-services-home/:/data/adaguc-services-home/ -v $HOME/esmvaltool_input:/root/esmvaltool_input -v $HOME/esmvaltool_output:/root/esmvaltool_output -it adaguc-services-compute
#docker exec -it  `docker ps -f ancestor=adaguc-services-compute -q` bash

# PyWPS log: /data/adaguc-services-home/adaguc-services-tmp/pywps.log

