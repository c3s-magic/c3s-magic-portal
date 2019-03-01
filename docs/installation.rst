Portal Installation
===================

This portal can be deployed with Docker. A docker compose file is present to start and orchestrate all the services needed. An .env file is used for settings, see the example file included.

Obtaining Docker and Docker Compose
-----------------------------------

The MAGIC portal is normally deployed using Docker. See `The Docker Documentation <https://docs.docker.com>`_ for more information on how to install and run docker.

In addition to docker, we also make use of `Docker Compose <https://docs.docker.com/compose/>`_.

Obtaining the portal code
-------------------------

The MAGIC portal code is available on GitHub. The main portal repo uses submodules as references to underlying services.

.. code-block:: sh

   $ git clone https://github.com/c3s-magic/c3s-magic-portal.git
   $ cd c3s-magic-portal
   $ git submodule init
   $ git submodule update

Creating a docker-compose .env file
-----------------------------------

The env file comes with an example (env.example). Copy this file .env and fill in the required fields

.. literalinclude:: ../env.example
   :language: sh


How to add a Metric
-------------------

1. Add recipe to ESMValTool
2. Fille in yaml settings file
3. Find out interactive plots options...
4. Profit!


## Deploying using docker-compose

 Add 127.0.1.1       portal.c3s-magic.eu to /etc/hosts    (portal.c3s-magic.eu is configured in console.developers.google.com for OAuth2 callback)
 Do docker-compose build --pull
 Do docker-compose up in working directory and go to localhost:80
 Do docker-compose down to stop all

#!/bin/bash

docker exec c3s-magic-portal_backend_1 /adaguc/adaguc-server-updatedatasets.sh
