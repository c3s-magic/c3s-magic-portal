# C3S-Magic Portal

This is the main repo of the C3S-Magic Portal software stack. It consists of a number of services, which together make up the Magic portal.

The Metrics and Access to Global Indices for Climate Projections (MAGIC) portal provides a quick and easy assessment of climate projections using well-established performance metrics. It allows the user to configure these criteria, apply them on selected CMIP5 model output and visualize results in the browser or download them onto your local machine.

Whom is this portal for?
This portal provides both metrics on model fidelity, targeted to climate scientists and meteorologists, as well as tailored products for different economic sectors, including insurances, agriculture, water management and sustainable energy.

This portal can be deployed with Docker. A docker compose file is present to start and orchestrate all the services needed. A .env file is used for settings, see the example file included.

The documentation for this portal (including an installation guide) can be found on readthedocs, at https://c3s-magic.readthedocs.io/en/latest/

Quick reminder: if you add static datasets to the server, be sure to tell adaguc about it:
```

#!/bin/bash

docker exec c3s-magic-portal_backend_1 /adaguc/adaguc-server-updatedatasets.sh

```
