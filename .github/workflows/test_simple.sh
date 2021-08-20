#!/usr/bin/env bash

# fail on non-zero return code from a subprocess
set -e

echo $PATH
which grass
grass_exe=$(which grass)

echo $grass_exe
cat $grass_exe

# grass --tmp-location EPSG:4326 --exec g.region res=0.1 -p
# grass --tmp-location EPSG:4326 --exec which t.create
# grass --tmp-location EPSG:4326 --exec t.create --help
