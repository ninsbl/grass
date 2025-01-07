
A variable in scripting is a symbolic name that holds data which can be
used and modified during script execution. Variables allow scripts to
store and manipulate values dynamically, making them more flexible and
reusable.
In GRASS GIS, there are two types of variables:

* [shell
  environment](#setting-shell-environment-variables) variables,
* [GRASS gisenv](#setting-grass-gisenv-variables)
  variables.

There are a number of *shell* environment variable groups:

* [variables
  for rendering](#list-of-selected-grass-environment-variables-for-rendering)
* [variables
  for internal use](#list-of-selected-internal-grass-environment-variables)

*Note:* Any setting which needs to be modifiable by a GRASS module
(e.g. MONITOR by *[d.mon](d.mon.html)*) has to be a GRASS
gisenv variable.

## Setting shell environment variables

Setting shell environment variables depends on the shell being used:

Bash:

```

export VARIABLE=value

```

Csh:

```

setenv VARIABLE value

```

Cmd.exe (Windows):

```

set VARIABLE=value

```

To set up shell environment variables permanently:

* To get personal BASH shell definitions (aliases, color listing option, ...)
  into GRASS, store them in:

  `$HOME/.grass8/bashrc`
* To get personal CSH shell definitions (aliases, color listing option, ...)
  into GRASS, store them in:

  `$HOME/.grass8/cshrc`

## Setting GRASS gisenv variables

Use *[g.gisenv](g.gisenv.html)* within GRASS. This permanently
predefines GRASS variables in the `$HOME/.grass8/rc` file (Linux, Mac, BSD, ...)
or in the `%APPDATA%\Roaming\GRASS8\rc` file (Windows) after the
current GRASS session is closed.

Usage:

```

g.gisenv set="VARIABLE=VALUE"

```

It looks unusual with two equals signs, but *g.gisenv* serves dual duty for
getting and setting GRASS variables.

If the user just specifies a variable name, it defaults to **get** mode.
For example:

```

g.gisenv MAPSET
PERMANENT

```

## List of selected (GRASS related) shell environment variables

> [ To be set from the terminal shell or startup scripts ]

GISBASE
directory where GRASS lives. This is set automatically by the
startup script.
GISRC
name of `$HOME/.grass8/rc` file. Defines the system wide value
when starting a GRASS session. Within a GRASS session, a temporary copy
of this file will be used.
GRASS\_ADDON\_PATH
[grass startup script, g.extension]

specifies additional path(s) containing local and/or custom GRASS
modules extra to the standard distribution.
GRASS\_ADDON\_BASE
[grass startup script]
 allows specifying additional GISBASE
for local GRASS modules (normally installed as GRASS Addons
by `g.extension` module) extra to standard
distribution. The default on GNU/Linux
is `$HOME/.grass8/addons`, on MS
Windows `%APPDATA%\Roaming\GRASS8\addons`.
GRASS\_ADDON\_ETC
[libgis, g.findetc]

specify paths where support files (etc/) may be found external to
standard distribution.
GRASS\_COMPATIBILITY\_TEST
[libgis]

By default it is not possible to run C modules with a libgis that has a
different `GIS_H_VERSION`, the compatibility test will exit with a
fatal error. Setting this variable to 0 (zero) with
`GRASS_COMPATIBILITY_TEST=0` allows the test to be passed with a
warning.
GRASS\_COMPRESSOR
[libraster]

the compression method for new raster maps can be set with the
environment variable GRASS\_COMPRESSOR. Supported methods are RLE,
ZLIB, LZ4, BZIP2, and ZSTD. The default is ZSTD if available,
otherwise ZLIB, which can be changed with e.g.
`GRASS_COMPRESSOR=ZSTD`, granted that GRASS has been
compiled with the requested compressor. Compressors that are always
available are RLE, ZLIB, and LZ4. The compressors BZIP2 and ZSTD
must be enabled when configuring GRASS for compilation.
GRASS\_CONFIG\_DIR
[grass startup script]

specifies root path for GRASS configuration directory.
If not specified, the default placement of the
configuration directory is used: `$HOME` on GNU/Linux,
`$HOME/Library` on Mac OS X, and `%APPDATA%` on MS Windows.
GRASS\_DB\_ENCODING
[various modules, wxGUI]

encoding for vector attribute data (utf-8, ascii, iso8859-1, koi8-r)
GIS\_ERROR\_LOG
If set, GIS\_ERROR\_LOG should be the absolute path to the log
file (a relative path will be interpreted relative to the process'
cwd, not the cwd at the point the user set the variable). If not
set, `$HOME/GIS_ERROR_LOG` is used instead. The file will
only be used if it already exists.
GRASS\_ERROR\_MAIL
set to any value to send user mail on an error or warning that
happens while stderr is being redirected.
GRASS\_FONT
[display drivers]

specifies the font as either the name of a font from
`$GISBASE/etc/fontcap` (or alternative fontcap file
specified by GRASS\_FONT\_CAP), or alternatively the full path to a
FreeType font file.
GRASS\_ENCODING
[display drivers]

the encoding to be assumed for text which is drawn using a
freetype font; may be any encoding know to *iconv*.
GRASS\_FONT\_CAP
[g.mkfontcap, d.font, display drivers]

specifies an alternative location (to `$GISBASE/etc/fontcap`) for
the font configuration file.
GRASS\_FULL\_OPTION\_NAMES
[parser]

Generates a warning if GRASS\_FULL\_OPTION\_NAMES is set (to anything) and
a found string is not an exact match for the given string.
GRASS\_GUI
either `text` (text user interface), `gtext` (text
user interface with GUI welcome screen), or `gui` (graphical
user interface) to define non-/graphical startup. Can also specify
the name of the GUI to use, e.g. `wxpython`
(*[wxGUI](wxGUI.html)*). Also exists as a GRASS
gisenv variable (see below). If this shell variable exists at GRASS
startup, it will determine the GUI used. If it is not defined
startup will default to the last GUI used.
GRASS\_HTML\_BROWSER
[init.sh, wxgui]
 defines name of HTML browser. For most
platforms this should be an executable in your PATH, or the full
path to an executable.
 Mac OS X runs applications differently
from the CLI. Therefore, GRASS\_HTML\_BROWSER should be the
application's signature, which is a domain-like name, just
reversed, i.e. com.apple.Safari. To find an application's
signature, type the following in a Terminal (fill in the path to
the application you are interested in, for example:
/Applications/Safari.app):
     `grep -A 1
"CFBundleIdentifier"` */path/to/application.app*`/Contents/Info.plist`

  The signature is the <string> following the
<key>, without the bracketing <string> tags.
GRASS\_INT\_ZLIB
[libraster]
 if the environment variable GRASS\_INT\_ZLIB exists and has the value 0,
new compressed *integer* (CELL type) raster maps will be compressed
using RLE compression.

If the variable doesn't exist, or the value is non-zero, zlib compression
will be used instead. Such rasters will have a `compressed`
value of 2 in the cellhd file.

Obviously, decompression is controlled by the
raster's `compressed` value, not the environment variable.
GRASS\_ZLIB\_LEVEL
[libgis]
 if the environment variable GRASS\_ZLIB\_LEVEL exists and its value can
be parsed as an integer, it determines the compression level used when new compressed
raster maps are compressed using zlib compression. This applies to all
raster map types (CELL, FCELL, DCELL).

Valid zlib compression levels are -1 to 9. The `GRASS_ZLIB_LEVEL=-1` corresponds
to the zlib default value (equivalent to `GRASS_ZLIB_LEVEL=6`). Often
`GRASS_ZLIB_LEVEL=1` gives the best compromise between speed and compression.

If the variable doesn't exist, or the value cannot be parsed as an
integer, zlib's default compression level 6 will be used.
GRASS\_MESSAGE\_FORMAT
[various modules, wxGUI]

it may be set to either

* `standard` - sets percentage output and message
  formatting style to standard formatting,
* `gui` - sets percentage output and message formatting
  style to GUI formatting,
* `silent` - disables percentage output and error
  messages,
* `plain` - sets percentage output and message
  formatting style to ASCII output without rewinding control
  characters.

GRASS\_MOUSE\_BUTTON
[various modules]
 swaps mouse buttons for two-button or
left-handed mice. Its value has three digits 1, 2, and 3, which
represent default left, middle, and right buttons
respectively. Setting to `132` will swap middle and right
buttons. Note that this variable should be set before a display
driver is initialized (e.g.,
`d.mon x0`).
GRASS\_PAGER
[various modules]

it may be set to either `less`, `more`, or `cat`.
GRASS\_PERL
[used during install process for generating man pages]

set Perl with path.
GRASS\_PROXY
[used during addon install/reinstall process for generating man
pages (download commit from GitHub API server and remote modules.xml file)]

set the proxy with: `GRASS_PROXY="http=<value>,ftp=<value>"`.
GRASS\_SKIP\_MAPSET\_OWNER\_CHECK
By default it is not possible to work with MAPSETs that are
not owned by current user. Setting this variable to any non-empty value
allows the check to be skipped.
GRASS\_SH
[shell scripts on Windows]

path to bourne shell interpreter used to run shell scripts.
GRASS\_SIGSEGV\_ON\_ERROR
Raise SIGSEGV if an error occurs]

This variable can be set for debugging purpose. The call
of G\_fatal\_error() will end in a segmentation violation. GDB can be used
to trace the source of the error.
GRASS\_PYTHON
[wxGUI, Python Ctypes]

set to override Python executable.

On Mac OS X this should be the `pythonw` executable for the
wxGUI to work.
GRASS\_VECTOR\_LOWMEM
[vectorlib]

If the environment variable GRASS\_VECTOR\_LOWMEM exists, memory
consumption will be reduced when building vector topology
support structures. Recommended for creating large vectors.
GRASS\_VECTOR\_OGR
[vectorlib, v.external.out]
 If the environment variable
GRASS\_VECTOR\_OGR exists and vector output format defined
by *[v.external.out](v.external.out.html)* is
PostgreSQL, vector data is written by OGR data provider even
the native PostGIS data provider is available.
GRASS\_VECTOR\_EXTERNAL\_IMMEDIATE
[vectorlib, v.external.out]
 If the environment variable
GRASS\_VECTOR\_EXTERNAL\_IMMEDIATE exists and vector output format
defined
by *[v.external.out](v.external.out.html)* is
non-native, vector features are written to output external
datasource immediately. By default, the vector library writes
output data to a temporary vector map in native format and when
closing the map, the features are transferred to output external
datasource. Note: if output vector format is topological PostGIS
format, then the vector library writes features immediately to output
database (in this case GRASS\_VECTOR\_EXTERNAL\_IMMEDIATE is ignored).
GRASS\_VECTOR\_EXTERNAL\_IGNORE
[vectorlib]
 If the environment variable
GRASS\_VECTOR\_EXTERNAL\_IGNORE exists, output vector format defined
by *[v.external.out](v.external.out.html)* is
ignored. The format is always native.
GRASS\_VECTOR\_TEMPORARY
[vectorlib]
 If the environment variable
GRASS\_VECTOR\_TEMPORARY exists, GRASS vector library will operate
on temporary vector maps. New vector maps will be created in
temporary directory (see GRASS\_VECTOR\_TMPDIR\_MAPSET variable), existing
vector maps will be read (if found) also from this directory. It
may be set to either:

* `keep` - the temporary vector map is not deleted when
  closing the map.
* `move` - the temporary vector map is moved to the
  current mapset when closing the map.
* `delete` - the temporary vector map is deleted when
  closing the map.

Default value is `keep`.
Note that temporary vector maps are not visible to the user
via *[g.list](g.list.html)*
or *[wxGUI](wxGUI.html)*. They are used
internally by the GRASS modules and deleted automatically when
GRASS session is quited.
GRASS\_VECTOR\_TMPDIR\_MAPSET
[vectorlib]
 By default GRASS temporary directory is located in
`$LOCATION/$MAPSET/.tmp/$HOSTNAME`. If GRASS\_VECTOR\_TMPDIR\_MAPSET is
set to '0', the temporary directory is located in TMPDIR
(environmental variable defined by the user or GRASS initialization
script if not given).

Important note: This variable is currently used only in vector
library. In other words the variable is ignored by raster or
raster3d library.
GRASS\_VECTOR\_TOPO\_DEBUG
[vectorlib, v.generalize]
 If the environment variable
GRASS\_VECTOR\_TOPO\_DEBUG
exists, *[v.generalize](v.generalize.html)* runs
in extremely slow debug mode.
GRASS\_WXBUNDLED
[wxGUI]

set to tell wxGUI that a bundled wxPython will be used.

When set, the wxGUI will not check the wxPython version, as this
function is incompatible with a bundled wxPython. It is up to the
packager to make sure that a compatible wxPython version is bundled.
GRASS\_WXVERSION
[wxGUI]

set to tell wxGUI which version of wxPython to use.

When set, the wxGUI will select the given wxPython version. It's
useful when multiple versions of wxPython are installed and the
user wants to run wxGUI with non-default wxPython version.
GRASS\_XTERM
[lib/init/grass-xterm-wrapper, lib/init/grass-xterm-mac]

set to any value (e.g. rxvt, aterm, gnome-terminal, konsole) to
substitute 'x-terminal-emulator' or 'xterm'. The Mac OS X app
startup defaults to an internal '$GISBASE/etc/grass-xterm-mac',
which emulates the necessary xterm functionality in
Terminal.app.
GRASS\_UI\_TERM
set to any value to use the terminal based parser.
GRASS\_VERSION
reports the current version number (used by R-stats interface etc);
should not be changed by user.
GRASS\_NO\_GLX\_PBUFFERS
[nviz]

set to any value to disable the use of GLX Pbuffers.
GRASS\_NO\_GLX\_PIXMAPS
[nviz]

Set to any value to disable the use of GLX Pixmaps.
OMP\_NUM\_THREADS
[OpenMP]

If OpenMP support is enabled this limits the number of threads.
The default is set to the number of CPUs on the system.
Setting to '1' effectively disables parallel processing.
TMPDIR, TEMP, TMP
[Various GRASS GIS commands and wxGUI]

The default wxGUI temporary directory is chosen from a
platform-dependent list, but the user can control the selection of
this directory by setting one of the TMPDIR, TEMP or TMP
environment variables Hence the wxGUI uses $TMPDIR if it is set,
then $TEMP, otherwise /tmp.

### List of selected GRASS environment variables for rendering

> [ In addition to those which are understood by
> specific *[GRASS display
> drivers](displaydrivers.html)*, the following variables affect rendering. ]

GRASS\_RENDER\_IMMEDIATE
tells the display library which driver to use; possible
values: *[cairo](cairodriver.html)*, *[png](pngdriver.html)*, *[ps](psdriver.html)*,
*[html](htmldriver.html)*
or *default*.
Default display driver
is *[cairo](cairodriver.html)* (if available)
otherwise *[png](pngdriver.html)*.

GRASS\_RENDER\_WIDTH
defines the width of output image (default is 640).
GRASS\_RENDER\_HEIGHT
defines the height of output image (default is 480).
GRASS\_RENDER\_FILE
the name of the resulting image file.
GRASS\_RENDER\_FRAME
contains 4 coordinates, *top,bottom,left,right* (pixel
values) with respect to the top left corner of the output image,
defining the initial frame.
GRASS\_RENDER\_LINE\_WIDTH
defines default line width.
GRASS\_RENDER\_TEXT\_SIZE
defines default text size.
GRASS\_RENDER\_COMMAND
external command called by display library to render data (see
example in *[display
drivers](displaydrivers.html)* page for details).
Currently only Python scripts
are supported.

For specific driver-related variables see:

* *[Cairo display driver](cairodriver.html)*
* *[PNG display driver](pngdriver.html)*
* *[PS (Postscript) display driver](psdriver.html)*
* *[HTML display driver](htmldriver.html)*

### List of selected internal GRASS environment variables

> [ These variables are intended **for internal use only** by the GRASS
> software to facilitate communication between the GIS engine, GRASS scripts,
> and the GUI.
> The user should not set these in a GRASS session. They are meant to be set
> locally for specific commands. ]

GRASS\_OVERWRITE
[all modules]

toggles map overwrite.

* 0 - maps are protected (default),
* 1 - maps with identical names will be overwritten.

This variable is automatically created
by *[g.parser](g.parser.html)* so that the
`--overwrite` option will
be inherited by dependent modules as the script runs. Setting either the
GRASS\_OVERWRITE environment variable or the OVERWRITE gisenv variable detailed
below will cause maps with identical names to be overwritten.
GRASS\_VERBOSE
[all modules]

toggles verbosity level

* -1 - complete silence (also errors and warnings are discarded)
* 0 - only errors and warnings are printed
* 1 - progress and important messages are printed (percent complete)
* 2 - all module messages are printed
* 3 - additional verbose messages are printed

This variable is automatically created by *[g.parser](g.parser.html)*
so that the `--verbose` or `--quiet` flags will be inherited
by dependent modules as the script runs.
GRASS\_REGION
[libgis]

override region settings, separate parameters with a ";". Format
is the same as in the WIND region settings file. Otherwise use is the same as
WIND\_OVERRIDE.
WIND\_OVERRIDE
[libgis]

it causes programs to use the specified named region (created with
e.g. `g.region save=...`) to be used as the current region, instead of
the region from the WIND file.

This allows programs such as the GUI to run external commands on an
alternate region without having to modify the WIND file then change it
back afterwards.

## List of selected GRASS gisenv variables

> [ Use *[g.gisenv](g.gisenv.html)* to get/set/unset/change them ]

DEBUG
[entire GRASS]

sets level of debug message output (0: no debug messages)

```

g.gisenv set=DEBUG=0

```

WX\_DEBUG
[wxGUI]

sets level of debug message output for *[wxGUI](wxGUI.html)* (0: no debug messages, 1-5 debug levels)
GISDBASE
initial database
GIS\_LOCK
lock ID to prevent parallel GRASS use,

process id of the start-up shell script
GUI
See `GRASS_GUI` environmental variable for details.
LOCATION
full path to project (previously called location) directory
LOCATION\_NAME
initial project name
MAPSET
initial mapset
MEMORYMB
[entire GRASS with focus on raster related data processing]

sets the maximum memory to be used (in MB), i.e. the cache size for raster rows

```

# set to 6 GB (default: 300 MB)
g.gisenv set="MEMORYMB=6000"

```

NPROCS
sets the number of threads for parallel computing

```

# set to use 12 threads (default: 1)
g.gisenv set="NPROCS=12"

```

OVERWRITE
[all modules]

toggles map overwrite.

* 0 - maps are protected (default),
* 1 - maps with identical names will be overwritten.

This variable is automatically created
by *[g.parser](g.parser.html)* so that the
`--overwrite` option will
be inherited by dependent modules as the script runs. Setting either the
GRASS\_OVERWRITE environment variable or the OVERWRITE gisenv variable detailed
below will cause maps with identical names to be overwritten.

## GRASS-related Files

`$HOME/.grass8/rc`
stores the GRASS gisenv variables (not shell environment variables)
`$HOME/.grass8/bashrc`
stores the shell environment variables (Bash only)
`$HOME/.grass8/env.bat`
stores the shell environment variables (MS Windows only)
`$HOME/.grass8/login`
stores the DBMI passwords in this hidden file.
Only the file owner can access this file.
`$HOME/GIS_ERROR_LOG`
if this file exists then all GRASS error and warning messages are
logged here. Applies to current user. To generate the file, use:
`touch $HOME/GIS_ERROR_LOG`

See also GIS\_ERROR\_LOG variable.

Note: On MS Windows the files are stored in `%APPDATA%`.

## SEE ALSO

*[g.gisenv](g.gisenv.html),
[g.parser](g.parser.html)*
