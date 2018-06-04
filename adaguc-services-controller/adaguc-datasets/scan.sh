#!/bin/bash

folder=WP7_BSC_ACI_Components

for file in /data/adaguc-data/c3smagic/${folder}/*nc; do
echo "<!-- $file -->"
 ~/code/maartenplieger/adaguc-server/bin/adagucserver --getlayers --file ${file} --datasetpath ${file}

done
