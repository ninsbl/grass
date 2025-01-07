
*Cairo display driver* for bitmap or vector output using the
Cairo graphics library.

## DESCRIPTION

The Cairo driver generates PNG, BMP, PPM, PS, PDF or SVG images by
GRASS display commands, using the
[Cairo graphics library](https://www.cairographics.org/).
The image format is selected from the extension of the output file.
The Cairo driver is used for GRASS display commands by default if
available, otherwise *[PNG driver](pngdriver.html)*
is used.

## USAGE

### Environment variables

The Cairo driver can be enabled by
setting **GRASS\_RENDER\_IMMEDIATE** variable, eg.

```

export GRASS_RENDER_IMMEDIATE=cairo

```

Several environment variables affect the operation of the Cairo driver:

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
* **GRASS\_RENDER\_ANTIALIAS**
   can be *default*,
  *none*, *gray*, or *subpixel*, corresponding to
  [cairo\_antialias\_t](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-antialias-t)
* **GRASS\_RENDER\_FILE=filename**

  the name and format of the resulting image file, default is
  `map.png`.

  The image format is determined from the file extension.

  Supported bitmap formats:
    * **.png** - Portable Network Graphics (PNG)
    * **.bmp** - Windows Bitmap (BMP, 32-bpp)
    (these are not readable by some older viewers)
    * **.ppm** - Portable Pixmap (PPM + PGM for alpha channel)Supported vector formats:
    * **.pdf** - Portable Document Format (PDF)
    * **.ps** - PostScript (PS)
    * **.svg** - Scalable Vector Graphics (SVG)(Note: Some formats may not be available, depending on your platform and
  the Cairo library that GRASS was built with.)
* **GRASS\_RENDER\_FILE\_READ**

  if `TRUE`, the Cairo driver will initialize the image from
  the contents of GRASS\_RENDER\_FILE.

  (*Note: This is only supported for bitmap formats*)
* **GRASS\_RENDER\_FILE\_MAPPED**

  if `TRUE`, the Cairo driver will map GRASS\_RENDER\_FILE as its framebuffer,
  rather than using memory.

  (*Note: This only works with BMP files.*)
* **GRASS\_RENDER\_CAIRO\_SCREEN**

  defines Cairo screen
* **GRASS\_RENDER\_CAIRO\_VISUAL**

  defines Cairo visual

## EXAMPLES

### PNG Example

Example: using the driver to generate a PNG file (bash-syntax):

```

export GRASS_RENDER_IMMEDIATE=cairo
export GRASS_RENDER_FILE=nc_spm.png
export GRASS_RENDER_WIDTH=800
export GRASS_RENDER_HEIGHT=800
export GRASS_RENDER_FILE_READ=TRUE

g.region raster=elevation
d.rast map=elevation
d.vect map=streams width=1 color=blue fcolor=aqua type=area,line
d.vect map=roadsmajor width=2

```

### PDF Examples

Example: using the driver to generate a PDF vector file with a vector
map (bash-syntax):

```

export GRASS_RENDER_IMMEDIATE=cairo
export GRASS_RENDER_FILE=nc_spm.pdf
export GRASS_RENDER_WIDTH=800
export GRASS_RENDER_HEIGHT=800

g.region vector=roadsmajor
# activate vector font
d.font Vera
d.vect map=roadsmajor layer=1 display=shape attrcolumn=ROAD_NAME lcolor=0:90:255

```

Example: using the driver to generate a PDF raster file with a raster
map (bash-syntax):

```

export GRASS_RENDER_IMMEDIATE=cairo
export GRASS_RENDER_FILE=nc_spm.pdf
export GRASS_RENDER_WIDTH=800
export GRASS_RENDER_HEIGHT=800

g.region raster=elevation
d.rast map=elevation

```

### SVG Example

Example: using the driver to generate a SVG vector file with a vector
map (bash-syntax):

```

export GRASS_RENDER_IMMEDIATE=cairo
export GRASS_RENDER_FILE=vectormap.svg

g.region vector=roadsmajor
d.vect map=roadsmajor -c

```

## NOTES

The driver is still in development. Enable it by specifying
`--with-cairo` when configuring GRASS. This
requires a reasonably recent version of the Cairo libraries
and a working `pkg-config`.

Antialiasing is enabled by default for bitmap formats. There is
currently no way of disabling this.

The resolution of the output images is defined by current region
extents. Use `g.region -p` to get the number of rows and cols
and use the environment variables to set the image size. If you would
like a larger image, multiply both rows and cols by the same whole
number to preserve the aspect ratio.

Cairo supports true vector format output whenever possible. However,
if the selected format doesn't support a necessary feature, Cairo may
fall back on rendering a bitmap representation of the image wrapped in
the selected vector format.

## SEE ALSO

*[PNG driver](pngdriver.html),
[PS driver](psdriver.html),
[HTML driver](htmldriver.html),
[variables](variables.html)*

*[d.rast](d.rast.html),
[d.vect](d.vect.html),
[d.mon](d.mon.html),
[d.erase](d.erase.html),
[d.redraw](d.redraw.html)*

## AUTHOR

Lars Ahlzen <*lars (at) ahlzen.com*>

and the GRASS Development Team.
