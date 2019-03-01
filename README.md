# C3S-Magic Portal

This is the main repo of the C3S-Magic Portal software stack. It consists of a number of services, which together make up the Magic portal.

The documentation for this portal (including an installation guide) can be found on readthedocs, at https://c3s-magic.readthedocs.io/en/latest/

This portal can be deployed with Docker. A docker compose file is present to start and orchestrate all the services needed. A .env file is used for settings, see the example file included.


Quick reminder: if you add static datasets to the server, be sure to tell adaguc about it:
```

#!/bin/bash 

docker exec c3s-magic-portal_backend_1 /adaguc/adaguc-server-updatedatasets.sh

```
