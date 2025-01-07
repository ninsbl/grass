
*PS display driver* to create PostScript files.

## DESCRIPTION

The PS driver generates a PostScript file from GRASS display commands.

## USAGE

### Environment variables

The PS driver can be enabled by setting **GRASS\_RENDER\_IMMEDIATE**
variable, eg.

```

export GRASS_RENDER_IMMEDIATE=ps

```

Several environment variables affect the operation of the PS driver:

* **GRASS\_RENDER\_WIDTH=xxx**

  the width of the image map (default is 640).
* **GRASS\_RENDER\_HEIGHT=yyy**

  the height of the image map (default is 480).
* **GRASS\_RENDER\_TRUECOLOR=[TRUE|FALSE]**

  sets true-color support. Default is FALSE.
* **GRASS\_RENDER\_FILE**

  name of output file. If it ends with ".eps" an EPS file
  will be created.
* **GRASS\_RENDER\_PS\_PAPER**

  sets the screen dimensions and margins to
  fit a standard paper size, see also GRASS\_RENDER\_WIDTH, GRASS\_RENDER\_HEIGHT.
* **GRASS\_RENDER\_PS\_LANDSCAPE**

  if `TRUE`, the screen is rotated 90 degrees
  counter-clockwise so that a "landscape" screen fits better on
  "portrait" paper.
* **GRASS\_RENDER\_PS\_HEADER**

  if `FALSE`, the output is appended to any existing file,
  and no prolog or setup sections are generated.
* **GRASS\_RENDER\_PS\_TRAILER**

  if `FALSE`, no trailer section is generated.

### Example

```

export GRASS_RENDER_IMMEDIATE=ps
export GRASS_RENDER_TRUECOLOR=TRUE

g.region raster=elevation
d.rast elevation
d.vect roadsmajor color=red

```

This writes a file named `map.ps` in your current directory.

## NOTES

The resolution of the output files is defined by current region
extents. Use `g.region -p` to get the number of rows and cols
and use the environment variables to set the image size. If you would
like a larger image, multiply both rows and cols by the same whole
number to preserve the aspect ratio.

GRASS\_RENDER\_TRUECOLOR requires either PostScript level 2 or level 1 plus the
colorimage and setrgbcolor operators (this is the case for colour
printers which pre-date level 2 PostScript).

Masked images (`d.rast`, `d.rgb`, `d.his -n`)
require PostScript level 3.

## SEE ALSO

*[Cairo driver](cairodriver.html),
[PNG driver](pngdriver.html),
[HTML driver](htmldriver.html),
[variables](variables.html)*

*[d.rast](d.rast.html),
[d.vect](d.vect.html),
[d.mon](d.mon.html),
[d.erase](d.erase.html),
[d.redraw](d.redraw.html)*

## AUTHOR

Glynn Clements, 2007
