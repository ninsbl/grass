
*PNG display driver* to create PNG, PPM, or BMP images.

## DESCRIPTION

The PNG driver generates PNG, PPM, or BMP images from GRASS display
commands. Per default PNG files are written with this driver. This
driver is used by default if *[Cairo
driver](cairodriver.html)* is not available.

## USAGE


### Environment variables

The PNG driver can be enabled by setting **GRASS\_RENDER\_IMMEDIATE**
variable, eg.

```


export GRASS_RENDER_IMMEDIATE=png


```


Several environment variables affect the operation of the PNG driver:

* **GRASS\_RENDER\_WIDTH=xxx**

  the width of the image map (default is 640).
* **GRASS\_RENDER\_HEIGHT=yyy**

  the height of the image map (default is 480).
* **GRASS\_RENDER\_BACKGROUNDCOLOR=RRGGBB**

  specifies the background color to use in RGB notation (hex or
  R:G:B values). Named colors are also supported. Default
  is **FFFFFF** (white).
* **GRASS\_RENDER\_TRANSPARENT=[TRUE|FALSE]**

  sets transparent background on (TRUE) or off (FALSE, default).
* **GRASS\_RENDER\_TRUECOLOR=[TRUE|FALSE]**

  sets true-color support. Default is TRUE.
* **GRASS\_RENDER\_FILE=filename**

  the filename to put the resulting image in, default is `map.png`.
  If you set GRASS\_RENDER\_FILE to a filename which ends in ".ppm", a PPM
  file will be created (with alpha channel stored in a PGM image, if applicable).
  If you set GRASS\_RENDER\_FILE to a filename which ends in ".bmp", a 32-bpp
  BMP file will be created (these are not readable by some older viewers).
* **GRASS\_RENDER\_FILE\_COMPRESSION=[0|1|9]**

  compression level of PNG files (0 = none, 1 = fastest, 9 = best, default is 6)
* **GRASS\_RENDER\_FILE\_READ**

  if `TRUE`, the PNG driver will initialize the image from
  the contents of GRASS\_RENDER\_FILE.
* **GRASS\_RENDER\_FILE\_MAPPED**

  if `TRUE`, the PNG driver
  will map GRASS\_RENDER\_FILE as its framebuffer, rather than using
  memory. This only works with BMP files.


### Example


```


export GRASS_RENDER_IMMEDIATE=png
export GRASS_RENDER_TRUECOLOR=TRUE

g.region raster=elevation
d.rast elevation
d.vect roadsmajor color=red


```


This writes a file named `map.png` in your current directory.

## NOTES

The PNG driver uses the libpng (see
the [libpng](http://www.libpng.org/pub/png/) home page) and
zlib (see the
[zlib](http://www.zlib.net) home page), all which needs to
be installed for the PNG driver to work (it's worth it).

The resolution of the output images is defined by current region
extents. Use `g.region -p` to get the number of rows and cols
and use the environment variables to set the image size. If you would
like a larger image, multiply both rows and cols by the same whole
number to preserve the aspect ratio.

Further PNG file processing (e.g. quantization to 1 bit for monochrome
images) can be done with `pnmquant` of
the [netpbm](https://netpbm.sourceforge.net/) tools.

## SEE ALSO

*[Cairo driver](cairodriver.html),
[PS driver](psdriver.html),
[HTML driver](htmldriver.html),
[variables](variables.html)*

*[d.rast](d.rast.html),
[d.vect](d.vect.html),
[d.mon](d.mon.html),
[d.erase](d.erase.html),
[d.redraw](d.redraw.html)*

## AUTHORS

Original version: Per Henrik Johansen <*phj (at)
norgit.no*>

Rewritten by: Glynn Clements, 2003
