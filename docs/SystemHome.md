# System

This section lists some of the features of the C3S-Magic system. Note that the system is still very much in active development, and some features may not be available yet.

## Final System Description

<img src="/contents/images/C3S 34a System Overview - MAGIC Wps.png" width="700px">

The MAGIC Web Processing Service (WPS) provides the scientific functionality of MAGIC. Building on s2dverificatoin, climate explorer, iris, ESMValTool, pyWPS, and other libraries and tools, the WPS takes ESGF CMIP5 data and processes these into the graphs and data shown on this portal.

<img src="/contents/images/C3S 34a System Overview - Infrastructure.png" width="700px">

This is an overview of the infrastructure in which the WPS is running. It consists of the portal system based on Climate4Impact and ADAGUC Services. These run on cloud infrastructure outside of ESGS, and is managed by the MAGIC team.

The actual processing of ESGF data will be done on infrastructure provided by the CP4CD project.
