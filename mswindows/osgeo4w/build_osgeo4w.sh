#!/bin/sh

#
# Usage: build_osgeo4w.sh
#
# The following environment variables are supposed to be passed to the build script
# - SRC: the directory where the grass source code lives
# - OSGEO4W_ROOT_MSYS: the root directory of OSGeo4W
# - UNITTEST: If this variable is defined, addition files for unittests are created
#
# By default, the script will look for the source code in the current directory
# and create bin.x86_64-w64-mingw32\grass$ver.bat (run this batch file to start
# GRASS GIS) and dist.x86_64-w64-mingw32\etc\env.bat.
#
# -p	optionally install GRASS GIS to C:\OSGeo4W\opt\grass (run
#	C:\OSGeo4W64\opt\grass\grass$ver.bat) and create an unzippable package
#	grass$ver-x86_64-w64-mingw32-osgeo4w64-$date.zip
#
# path	specify a path to the source code
#

# stop on errors
# set -e


# compile
export VCPATH="$(cygpath "C:/Program Files (x86)/Microsoft Visual Studio/2019/Enterprise/VC/Tools/MSVC/14.29.30133/include")"
export PATH="${OSGEO4W_ROOT_MSYS}/bin:/usr/bin:/mingw64/bin"
export ARCH=x86_64-w64-mingw32
export C_INCLUDE_PATH=".:${OSGEO4W_ROOT_MSYS}/include:${SRC}/dist.${ARCH}/include:/c/msys64/mingw64/${ARCH}/include:/c/msys64/mingw64/include"
export CPLUS_INCLUDE_PATH=".:${OSGEO4W_ROOT_MSYS}/include:${SRC}/dist.${ARCH}/include:${VCPATH}"
# :/c/msys64/mingw64/${ARCH}/include:/c/msys64/mingw64/include:/c/msys64/mingw64/include/c++/10.3.0:/c/msys64/mingw64/include/c++"
export PYTHONHOME="${OSGEO4W_ROOT_MSYS}/apps/Python39"
export CPPFLAGS="-I${VCPATH} -I/c/msys64/mingw64/include/c++ -I/c/msys64/mingw64/${ARCH}/include -I/c/msys64/mingw64/include -I${OSGEO4W_ROOT_MSYS}/include -I${SRC}/dist.${ARCH}/include -I/usr/include"



./configure \
    --host=${ARCH} \
    --with-libs="${OSGEO4W_ROOT_MSYS}/lib ${OSGEO4W_ROOT_MSYS}/bin" \
    --with-includes=${OSGEO4W_ROOT_MSYS}/include \
    --libexecdir=${OSGEO4W_ROOT_MSYS}/bin \
    --prefix=${OSGEO4W_ROOT_MSYS}/apps/grass \
    --bindir=${OSGEO4W_ROOT_MSYS}/bin \
    --includedir=${OSGEO4W_ROOT_MSYS}/include \
    --without-x \
    --with-cxx \
    --enable-shared \
    --enable-largefile \
    --with-openmp \
    --with-fftw \
    --with-nls \
    --with-readline \
    --with-wxwidgets \
    --with-blas \
    --with-lapack-includes=/mingw64/include/lapack \
    --with-freetype \
    --with-freetype-includes=/mingw64/include/freetype2 \
    --with-proj-share=${OSGEO4W_ROOT_MSYS}/share/proj \
    --with-proj-includes=${OSGEO4W_ROOT_MSYS}/include \
    --with-proj-libs=${OSGEO4W_ROOT_MSYS}/lib \
    --with-postgres \
    --with-postgres-includes=${OSGEO4W_ROOT_MSYS}/include \
    --with-postgres-libs=${OSGEO4W_ROOT_MSYS}/lib \
    --with-gdal=${SRC}/mswindows/osgeo4w/gdal-config \
    --with-geos=${SRC}/mswindows/osgeo4w/geos-config \
    --with-pdal=${OSGEO4W_ROOT_MSYS}/bin/pdal-config \
    --with-sqlite \
    --with-sqlite-includes=${OSGEO4W_ROOT_MSYS}/include \
    --with-sqlite-libs=${OSGEO4W_ROOT_MSYS}/lib \
    --with-regex \
    --with-nls \
    --with-zstd \
    --with-odbc \
    --with-cairo \
    --with-cairo-includes=${SRC}/include \
    --with-cairo-ldflags="-L${SRC}/mswindows/osgeo4w/lib -lcairo -lfontconfig" \
    --with-opengl=windows \
    --with-bzlib \
    --with-liblas=${SRC}/mswindows/osgeo4w/liblas-config \
    --with-netcdf=${OSGEO4W_ROOT_MSYS}/bin/nc-config &> configure.log

printf "\nconfigure.log\n"
cat configure.log
printf "\nconfig.log\n"
cat config.log
