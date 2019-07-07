Portal Installation
===================

This portal can be deployed with Docker. A docker compose file is present to start and orchestrate all the services needed. An .env file is used for settings, see the example file included.

Obtaining Docker and Docker Compose
-----------------------------------

The MAGIC portal is normally deployed using Docker. See `The Docker Documentation <https://docs.docker.com>`_ for more information on how to install and run docker.

In addition to docker, we also make use of `Docker Compose <https://docs.docker.com/compose/>`_.

This Guide assumes a working installation of docker and docker-compose, and knowledge of this software.

Obtaining the portal code
-------------------------

The MAGIC portal code is available on GitHub. The main portal repo uses submodules as references to underlying services.

.. code-block:: sh

   $ git clone https://github.com/c3s-magic/c3s-magic-portal.git
   $ cd c3s-magic-portal
   $ git submodule init
   $ git submodule update

Obtaining the required data
---------------------------

The dataset needed can be downloaded on zenodo.

Choosing a WPS location
-----------------------

Choose either the build-in wps (and supply the needed CP4CDS CMIP and OBS data), or point to the CP4CDS WPS (prefered). The location of the WPS used can be set in the .env file (see below)

Creating a docker-compose .env file
-----------------------------------

All settings are done via a docker environment file. The env file comes with an example (env.example). Copy this file .env and fill in the required fields. The software is currently setup for CEDA account usage only.

.. literalinclude:: ../env.example
   :language: sh

Deploying using docker-compose
------------------------------

Once the settings file is correctly filled in, the entire portal can be deployed with docker-compose like normal.

.. code-block:: sh

    $ docker-compose build --pull
    $ docker-compose up
    $ docker-compose down


Updating the ADAGUC Datasets
----------------------------

If the datasets served by ADAGUC are updated, update the database of these in the following manner:

.. code-block:: sh

    $ docker exec c3s-magic-portal_backend_1 /adaguc/adaguc-server-updatedatasets.sh
